from pymongo import MongoClient
import pymongo
import operator
import datetime
from bson.binary import Binary
import pickle
import numpy as np


def connect2Mongo(mongoInfo):
    client = MongoClient(mongoInfo['host'], mongoInfo['port'], username = mongoInfo['username'], password = mongoInfo['password'], authSource = mongoInfo['authDatabase'], authMechanism = mongoInfo['authMechanism'])
    callistoDB = client[mongoInfo['databaseName']]

    return client, callistoDB


def disconnectMongo(client):
    client.close()


def createAUAIRMongoRecord(response, shots_dir, categories, metadata):
    record = {}

    # Videoshot info
    record['shot_name'] = response['image_name']
    # Split image_name -> datetime + no_frame INSERT
    split_lst = response['image_name'].split('_')
    record['timestamp'] = split_lst[1]
    record['no_frame'] = int(split_lst[3].split('.')[0])
    record['shot_location'] = shots_dir + response['image_name']

    # Shot info
    if int(response['time']['ms']) > 999999:
        response['time']['ms'] = 999999

    record['datetime'] = datetime.datetime(response['time']['year'], response['time']['month'], response['time']['day'], response['time']['hour'], response['time']['min'], response['time']['sec'], int(response['time']['ms']))
    record['geoinformation'] = { 'type' : "Point", 'coordinates': [response['longtitude'], response['latitude']] }

    record['datetime_mp'] = [response['time']['year'], response['time']['month'], response['time']['day'], response['time']['hour'], response['time']['min'], response['time']['sec'], response['time']['ms']]
    record['geoinformation_mp'] = [response['longtitude'], response['latitude'], response['altitude']]

    shot_name_categories = []
    shot_id_categories = []
    for shot_object in response['bbox']:
        id_category = shot_object['class']
        name_category = categories[id_category]
        if id_category not in shot_id_categories:
            shot_id_categories.append(id_category)
            shot_name_categories.append(name_category)

    record['category_names'] = shot_name_categories
    record['category_ids'] = shot_id_categories

    # Fields useful for my service
    record['metadata'] = {}
    record['metadata']['visual_feature'] = metadata[0].tolist() #Binary(pickle.dumps(metadata[0], protocol=2), subtype=128)
    record['metadata']['temporal_feature'] = metadata[1].tolist() #Binary(pickle.dumps(metadata[1], protocol=2), subtype=128)
    record['metadata']['spatial_feature'] = metadata[2].tolist() #Binary(pickle.dumps(metadata[2], protocol=2), subtype=128)
    record['metadata']['visual_bin_vec'] = metadata[3].tolist() #Binary(pickle.dumps(metadata[3], protocol=2), subtype=128)
    record['metadata']['temporal_bin_vec'] = metadata[4].tolist() #Binary(pickle.dumps(metadata[4], protocol=2), subtype=128)
    record['metadata']['spatial_bin_vec'] = metadata[5].tolist() #Binary(pickle.dumps(metadata[5], protocol=2), subtype=128)

    return record['shot_name'], record


def insertRecordIfNotExists(productName, record, collection):
    productInserted = False

    doc = collection.find_one({'shot_name': productName})

    if doc == None:
        collection.insert_one(record)
        productInserted = True


    return productInserted


def getShotHashCodeBasedOnId(collection, queryId, modality):
    result = collection.find({'shot_name': queryId})
    hashCode = None
    numModalities = len(modality) 

    if numModalities == 1:
        for doc in result:
            hashCode = np.array(doc['metadata'][modality[0] + '_bin_vec']).astype(int)
    elif numModalities == 2:
        for doc in result:
            hashCode1 = np.array(doc['metadata'][modality[0] + '_bin_vec']).astype(int)
            hashCode2 = np.array(doc['metadata'][modality[1] + '_bin_vec']).astype(int)
            hashCode = np.bitwise_xor(hashCode1, hashCode2) 
    elif numModalities == 3:
        for doc in result:
            hashCode1 = np.array(doc['metadata'][modality[0] + '_bin_vec']).astype(int)
            hashCode2 = np.array(doc['metadata'][modality[1] + '_bin_vec']).astype(int)
            hashCode3 = np.array(doc['metadata'][modality[2] + '_bin_vec']).astype(int)
            hashCode = np.bitwise_and(np.bitwise_xor(hashCode1, hashCode2), np.bitwise_xor(hashCode1, hashCode3), np.bitwise_xor(hashCode2, hashCode3))
    else:
        raise ValueError('Unsupported number of modality')

    return hashCode.reshape(1, -1)


def getAllShotsHashCodeExcludingQueryId(collection, modality, queryId):
    # Get all documents except query
    results = collection.find({'shot_name': {'$ne': queryId}})
    hashCodes = []
    shotsId = []
    numModalities = len(modality)

    if numModalities == 1:
        for doc in results:
            shotId = doc['shot_name']
            hashCode = np.array(doc['metadata'][modality[0] + '_bin_vec']).astype(int).reshape(1, -1) 

            hashCodes.append(hashCode)
            shotsId.append(shotId)
    elif numModalities == 2:
        for doc in results:
            shotId = doc['shot_name']
            hashCode1 = np.array(doc['metadata'][modality[0] + '_bin_vec']).astype(int).reshape(1, -1) 
            hashCode2 = np.array(doc['metadata'][modality[1] + '_bin_vec']).astype(int).reshape(1, -1) 
            hashCode = np.bitwise_xor(hashCode1, hashCode2).reshape(1, -1)

            hashCodes.append(hashCode)
            shotsId.append(shotId)
    elif numModalities == 3:
        for doc in results:
            shotId = doc['shot_name']
            hashCode1 = np.array(doc['metadata'][modality[0] + '_bin_vec']).astype(int).reshape(1, -1) 
            hashCode2 = np.array(doc['metadata'][modality[1] + '_bin_vec']).astype(int).reshape(1, -1) 
            hashCode3 = np.array(doc['metadata'][modality[2] + '_bin_vec']).astype(int).reshape(1, -1) 
            hashCode =  np.bitwise_and(np.bitwise_xor(hashCode1, hashCode2), np.bitwise_xor(hashCode1, hashCode3), np.bitwise_xor(hashCode2, hashCode3)).reshape(1, -1)

            hashCodes.append(hashCode)
            shotsId.append(shotId)
    else:
        raise ValueError('Unsupported number of modality')

    return shotsId, np.vstack(hashCodes)


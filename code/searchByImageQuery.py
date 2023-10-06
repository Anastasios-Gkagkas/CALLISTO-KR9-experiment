from mongoFuncs import connect2Mongo, disconnectMongo, getShotHashCodeBasedOnId, getAllShotsHashCodeExcludingQueryId
from utils import getResultsNum 


def searchByImageQuery(queryId, modality, collection, resultsNum):
    # Mongo information
    print('Mongo info')
    mongoInfo = {}
    mongoInfo['username'] = 'root'
    mongoInfo['password'] = '123'
    mongoInfo['host'] = 'mongodb'
    mongoInfo['port'] = 27017
    mongoInfo['authMechanism'] = 'SCRAM-SHA-1'
    mongoInfo['databaseName'] = 'callisto'
    mongoInfo['authDatabase'] = 'admin'
    mongoInfo['collectionName'] = collection # AU-AIR or CALLISTO

    # Connect to Mongo
    print('Connect mongodb')
    client, callistoDB = connect2Mongo(mongoInfo)
    print(client)
    print(callistoDB)

    # Get binary vectors
    print('Get hash codes')
    queryCode = getShotHashCodeBasedOnId(callistoDB[collection], queryId, modality)
    print('getShots')
    shotsId, databaseCodes = getAllShotsHashCodeExcludingQueryId(callistoDB[collection], modality, queryId)

    # Query to Mongo. Find resultsNum relevant to query documents.
    results = getResultsNum(shotsId, queryCode, databaseCodes, resultsNum)

    # Disconnect Mongo
    print('Disconnect mongodb')
    disconnectMongo(client)

    return results

from __future__ import print_function
from json import dumps
from bottle import route, run, template, request, response
import searchByImageQuery as sq


@route('/MultimodalRetrievalServiceCallisto')
def index():
	print(request.query)
	#millisStart = time.time()
	queryId = request.query.image_id
	modality = request.query.modality.split(',')
	collection = request.query.collection
	resultsNum = int(request.query.limit)
	
	print(queryId)
	print(modality)
	print(collection)
	print(resultsNum)


	retrieved_results = sq.searchByImageQuery(queryId, modality, collection, resultsNum)
	output = retrieved_results.tolist()
	
	#print(type(output))
	#print(len(output))
	#print(output)
		
	response.content_type = 'application/json'
	response.headers['Access-Control-Allow-Origin'] = '*'
	return dumps(output)

#run(host='160.40.53.88', port=9006)
run(host='0.0.0.0', port=9005)

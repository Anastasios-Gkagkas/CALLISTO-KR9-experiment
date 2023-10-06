This document contains helpful information for running the service, the code for feature extraction and training procedure. 

We use python 3.8.10 and Ubuntu 20.04 for our implementation.

0. Setting MongoDB
	-Read instructions of set_mongodb.txt
	
1. Running service
	- Run command: 
		python3 multimodalFusionServiceForSingleImage.py
	- Open a browser and copy paste something like the following formats and press ENTER:
		- http://160.40.53.88:9005/MultimodalRetrievalServiceCallisto?image_id=frame_20190829091111_x_0001973.jpg&modality=visual&modality=temporal&collection=AU_AIR&limit=100
		- http://160.40.53.88:9005/MultimodalRetrievalServiceCallisto?image_id=frame_20190829091111_x_0001973.jpg&modality=visual,temporal&collection=AU_AIR&limit=100
		- http://160.40.53.88:9005/MultimodalRetrievalServiceCallisto?image_id=frame_20190829091111_x_0001973.jpg&modality=visual,spatial,temporal&collection=AU_AIR&limit=100
		
	    with image_id the frame name, modality the type of query and limit the number of returned images
	
2. Running code for feature extraction


3. Running code for training procedure


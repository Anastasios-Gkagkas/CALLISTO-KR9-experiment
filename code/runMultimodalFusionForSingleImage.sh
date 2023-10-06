TITLE MULTIMODAL SERVICE FOR CALLISTO
#REM  Service URL: http://160.40.53.88:9005/MultimodalRetrievalServiceCallisto?image_id=frame_20190829091111_x_0001973.jpg&modality=visual&modality=temporal&collection=AU_AIR&limit=100
REM  Service URL: http://160.40.53.88:9005/MultimodalRetrievalServiceCallisto?image_id=frame_20190829091111_x_0001973.jpg&modality=visual,temporal&collection=AU_AIR&limit=100
#REM  Service URL: http://160.40.53.88:9005/MultimodalRetrievalServiceCallisto?image_id=frame_20190829091111_x_0001973.jpg&modality=visual,spatial,temporal&collection=AU_AIR&limit=100

d:
cd /home/mpegia/MyProjects/multimodalFusionPerImage/
source env/bin/activate
multimodalFusionServiceForSingleImage.py



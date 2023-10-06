# How to run
In the root folder of the project run:
```
docker-compose up -d --build
```

# How to test

Example 1:
```
curl "http://localhost:9005/MultimodalRetrievalServiceCallisto?image_id=rgb_cral_day2_mission1_61.jpg&modality=visual,temporal&collection=callisto&limit=100"
```
Example 2:
```
curl "http://localhost:9005/MultimodalRetrievalServiceCallisto?image_id=rgb_cral_day1_mission2_116.jpg&modality=visual&collection=callisto&limit=50"
```

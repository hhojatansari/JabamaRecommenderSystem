# Jabama Recommender System


 ### Quick Start
 ```
 git clone https://github.com/hhojatansari/JabamaRecommenderSystem.git
 cd JabamaRecommenderSystem
 python -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.txt
 uvicorn main:app
```

### Deploy on docker
```
git clone https://github.com/hhojatansari/JabamaRecommenderSystem.git
cd JabamaRecommenderSystem
docker-compose build
docker-compose up -d
```


 ### Test
>
> Endpoint: `http://localhost:8000` \
> Swagger UI: `http://localhost:8000/swagger-ui`

product: `cottage-475984` \
recommendations number: `10`
```
curl -X 'GET' \
'http://localhost:8000/recommendations/cottage-475984?number=10' \
-H 'accept: application/json'
```
Request URL: `http://localhost:8000/recommendations/cottage-475984?number=10` 
 

#### Tested on 
- Ubuntu 24.04.1 LTS
- Python 3.12.3 

__author__      = "HHojatAnsari@gmail.com"

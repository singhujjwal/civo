# URL shortener service

This microservice app will be responsible for returning the shortened url
Will try to learn few tech as part of this excerise

1. KAFKA
2. REDIS
3. CASSANDRA as well 


All pluggable module as KAFKA docker can be replaced with MSK
REDIS with Elsticcache or redis cache
CASSANDRA with DynamoDB


## Design

## pre-reqs

Dont forget to export the below variables for using REDIS cache

export REDIS_HOST='xxxxxx'
export REDIS_PORT=16262
export REDIS_PASSWORD=passwordlongone



####

`docker build -t singhujjwal/url-service:0.3 .`
`docker image push singhujjwal/url-service:0.3`
```
docker run \
    --network  kafka_default \
    --env REDIS_HOST --env REDIS_PORT --env REDIS_PASSWORD \
    --env KAFKA_BOOTSTRAP_SERVERS='kafka:9092' \
    -it --rm --name urls -w /app -p 8121:8121 \
    singhujjwal/url-service:0.3  uvicorn app.main:app \
    --reload --host 0.0.0.0 --port 8121
```
`docker image push singhujjwal/url-service:0.2`


kubectl port-forward svc/urlservice 8081:80 
kubectl port-forward deployment/redis-master 6379:6379 
kubectl port-forward pods/redis-asdasd 6379:6379 
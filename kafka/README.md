


# first build and push the docker

`docker build -t singhujjwal/consumer:0.1 .`
`docker image push singhujjwal/consumer:0.1`


## Test the docker in exec mode later run in disconnected mode, better use docker compose
```
export KAFKA_BOOTSTRAP_SERVERS='kafka:9092'
docker run \
    --network  kafka_default \
    --env REDIS_HOST --env REDIS_PORT --env REDIS_PASSWORD \
    --env KAFKA_BOOTSTRAP_SERVERS='kafka:9092' \
    -it --rm --name consumer -w /app -p 8122:8122 \
    singhujjwal/consumer:0.1 uvicorn app.main:app \
    --reload --host 0.0.0.0 --port 8122
```
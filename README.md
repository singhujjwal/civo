This is not a twelve factor app but it should be 

https://12factor.net/
https://12factor.net/codebase

# URL shortener service
Most popular interview question, although the logic is quite straight forward but trying it into code is not.
It took me sometime to devote some time over here to setup components piece by piece.

1. KAFKA
2. REDIS
3. DB (Cassandra, Dynamodb ?? TBD)
4. Kafka running via docker-compose will be putting this stuff on k8s as well.
5. End to end k8s solution
6. Will try to include a end to end deployment on AWS using terraform and helm and further argocd and fluxcd for continous deployment
7. Try Blue/Green, canary deployment and also put istio
8. K8s operator and what not ???

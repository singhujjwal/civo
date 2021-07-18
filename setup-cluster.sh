#!/bin/bash


chmod go-r ~/.kube/config

CLUSTER_NAME="test"

echo "Setting up the whole cluster "
echo "Later just bootstrap the cluster and setup all components individually"

echo "######################################"
echo "Setup longhorn portal"
kubectl apply -f longhorn/longhorn-ingress.yaml
sleep 10
kubectl get ing -n longhorn-system

echo "Above is the longhorn url can be accessed"

echo "#############################################"
echo "setup ingress to kubernetes dashboard"


echo "############################################"
echo "Setting up portainer.............."
kubectl apply -f portainer/portainer-ingress.yaml
sleep 10
kubectl get ing -n portainer
# setup a password from script currently doing it from portal bruhh
echo "Kafka is already setup from civo portal and no ingress is needed as it is needed internally"


echo "Setup Mongo for external access............"
echo "No external HTTP directly, will investigate the http based management console if any present...."


kubectl create ns url

# this is a local file to export envs
# Think of loading it into sealed secrets

source ./env.sh.local
kubectl create secret generic redis-details \
    --from-literal=REDIS_HOST="${REDIS_HOST}" \
    --from-literal=REDIS_PORT="${REDIS_PORT}" \
    --from-literal=REDIS_PASSWORD="${REDIS_PASSWORD}" -n url

SYSTEM_NAMESPACE="kube-system"

kubectl create secret docker-registry ujjwaldocker --docker-server=hub.docker.com \
    --docker-username="${DOCKER_USER}" --docker-password="${DOCKER_PASSWORD}"  || true

kubectl replace serviceaccount default -f k8s-run/url-serviceaccount.yaml -n url

kubectl api-resources --verbs=list --namespaced -o name \
  | xargs -n 1 kubectl get --show-kind --ignore-not-found -n url

#Create frontend resources

kubectl apply -f k8s-run/frontend/

sleep 60
# Create the consumer service

kubectl apply -f k8s-run/db-mq/

sleep 60

# run test
kubectl apply -f k8s-run/test/loadrunner.yaml

echo "Sleep for 1 minute"

echo "Check for logs"
kubectl logs -l app=urlservice -n url
sleep 120
echo "Scale up the load to see the hpa kicking in.."
kubectl scale deployment.v1.apps/loadrunner --replicas=5 -n url
sleep 120
echo "Stop the load"
kubectl delete -f k8s-run/test/loadrunner.yaml


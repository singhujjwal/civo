#!/bin/bash


chmod go-r ~/.kube/config

CLUSTER_NAME="test"

echo "Wait for 3 minutes to get cluster up fully..."
sleep 180

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



echo "Setup a longhorn ingress........"
kubectl apply -f longhorn/longhorn-ingress.yaml

echo "Setup a Portainer ingress........"
kubectl apply -f portainer/portainer-ingress.yaml


#Create frontend resources
kubectl apply -f k8s-run/frontend/

sleep 30
# Create the consumer service

kubectl apply -f k8s-run/db-mq/

sleep 30

# run test
kubectl apply -f k8s-run/test/loadrunner.yaml

echo "Sleep for 2 minute"
echo "Check for logs"
sleep 120
kubectl logs -l app=urlservice -n url
echo "Scale up the load to see the hpa kicking in.."
kubectl scale deployment.v1.apps/loadrunner --replicas=3 -n url

# HPA directly
# kubectl autoscale deployment/urlconsumer --min=3 --max=6 --cpu-percent=80 -n url
sleep 180
echo "Stop the load"
# instead of deleting scale down the deployment
kubectl delete -f k8s-run/test/loadrunner.yaml
kubectl scale deployment.v1.apps/loadrunner --replicas=0 -n url


# helm repo add appscode https://charts.appscode.com/stable/ && helm repo update && helm search repo appscode/kubed
# helm install kubed appscode/kubed --version v0.12.0 \
#   --namespace "${SYSTEM_NAMESPACE}" \
#   --set apiserver.ca="$(onessl get kube-ca --analytics=false)" \
#   --set config.clusterName="${CLUSTER_NAME}" \
#   --set resources.requests.cpu="50m" \
#   --set resources.requests.memory="256Mi" \
#   --set resources.limits.cpu="100m" \
#   --set resources.limits.memory="1024Mi"

chmod go-r ~/.kube/config

CLUSTER_NAME="test"
kubectl create ns url
kubectl create secret generic redis-details \
    --from-literal=REDIS_HOST="${REDIS_HOST}" \
    --from-literal=REDIS_PORT="${REDIS_PORT}" \
    --from-literal=REDIS_PASSWORD="${REDIS_PASSWORD}" -n url

SYSTEM_NAMESPACE="kube-system"

helm repo add appscode https://charts.appscode.com/stable/ && helm repo update
helm install kubed appscode/kubed \
  --version v0.12.0 \
  --namespace kube-system

kubectl create secret docker-registry ujjwaldocker --docker-server=hub.docker.com \
    --docker-username="${DOCKER_USER}" --docker-password="${DOCKER_PASSWORD}"  || true

kubectl annotate secret ujjwaldocker kubed.appscode.com/sync=""
kubectl annotate secret redis-details kubed.appscode.com/sync="" -n url

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx --namespace ingress-nginx ingress-nginx/ingress-nginx \
--set controller.enableCustomResources=true --set controller.enableTLSPassthrough=true
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
# kubectl patch svc argocd-server  argocd -p '{"spec": {"type": "ClusterIP"}}'            


# finally couldnt bring it to work, even with nginx in passthrough mode tls so best is 
kubectl port-forward svc/argocd-server -n argocd 8080:443
and access it on the localhost:8080


kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
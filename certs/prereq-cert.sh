#!/bin/bash
helm install webhook-civo https://storage.googleapis.com/charts.okteto.com/cert-manager-webhook-civo-0.1.0.tgz --namespace=cert-manager

kubectl create secret generic civo-secret --from-literal=api-key=<YOUR_CIVO_TOKEN> -n cert-manager


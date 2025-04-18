# mpo-api-search-fastapi
MPO API Webservice focused on search functionality, using FastAPI and Python.

*Disclaimer*: Used various AI tools to learn how to set this up from within VS Code (Amazon Q, Gemini 2.0 Flash, GPT-4o, Claude 3.5 Sonnet) 

# Building docker image
## Install Docker
https://www.docker.com/get-started/

## Create a buildx builder (if not already created)
docker buildx create --use --name mybuilder

## Build the image
docker buildx build -t mpo-api-search-fastapi:latest --load .

# Running on a local cluster
The following are instructions for deploying to a local cluster via docker, kind, kubectl, and kubernetes. 

Currently working on a MacBook Pro (16in, M4 Pro, 48gb RAM, OS 15.3.2). Your results may vary.

## Install kind
brew install kind

## Install kubectl
brew install kubectl

## Create a kind cluster
kind create cluster --config=k8s/cluster.yaml

## Setup Ingress (Using nginx)
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml

## Wait for Ingress to be setup
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

## Load the image into the kind cluster
kind load docker-image mpo-api-search-fastapi:latest --name mpo-api-search-fastapi-cluster

## Apply the deployment and service manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

## Verify the deployment
kubectl get all

## Access the application
curl "http://localhost/search/?term=games"

## View logs (if desired)
kubectl logs -f deployment/mpo-api-search-fastapi-deployment

## To cleanup when done
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/ingress.yaml
kind delete cluster --name mpo-api-search-fastapi-cluster
# mpo-api-search-fastapi
![Coverage](https://github.com/{username}/{repository}/actions/artifacts/coverage.svg)

MPO API Webservice focused on search functionality, using FastAPI and Python.
Also contains instructions for local deployment using Docker, Kubernetes, and kind (Kubernetes in Docker)

***Disclaimer***: Used various AI tools to learn how to set this up from within VS Code (Amazon Q, Gemini 2.0 Flash, GPT-4o, Claude 3.5 Sonnet) 

## Run locally
```
pipenv install -r dev-requirements.txt
pipenv shell
python run.py
```

## Building docker image
### Install Docker
https://www.docker.com/get-started/

### Create a buildx builder (if not already created)
`docker buildx create --use --name mybuilder`

### Build the image
`docker buildx build -t mpo-api-search-fastapi:latest --load .`

## Running on a local cluster
See this repo for how this can be used in a local cluster environment with Kubernetes
https://github.com/hitoshura25/mpo-api-gateway
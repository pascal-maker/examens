# Docker build tutorial

## Build commands

- Basic: `docker build -t docker-build-demo:1 -f Dockerfile.1 .`
- Intermediate: `docker build -t docker-build-demo:2 -f Dockerfile.2 .`
- Advanced (multi-stage): `docker build -t docker-build-demo:3 -f Dockerfile.3 .`
- Alpine: `docker build -t docker-build-demo:4 -f Dockerfile.4 .`
- Alpine with args: `docker build -t docker-build-demo:5 -f Dockerfile.5 --build-arg FASTAPI_PORT=8080 .`

## Run commands

- Basic: `docker run -it -p 8000:8000 docker-build-demo:1`
- Intermediate: `docker run -it -p 8000:8000 docker-build-demo:2`
- Advanced (multi-stage): `docker run -it -p 8000:8000 docker-build-demo:3`
- Alpine: `docker run -it -p 8000:8000 docker-build-demo:4`
- Alpine with args: `docker run -it -p 8080:8080 docker-build-demo:5`

## Tests and explanation

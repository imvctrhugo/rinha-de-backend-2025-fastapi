# list all targets and exit
default: 
    just --list

# run locally using docker-compose
up *flags="": 
    docker compose up --build {{flags}}

# Publish multi-arch image to Docker Hub
publish image:
    docker buildx build \
      --platform linux/amd64,linux/arm64 \
      -t vctrhugo3011/rinha2025-{{image}}:latest \
      --push ./{{image}}

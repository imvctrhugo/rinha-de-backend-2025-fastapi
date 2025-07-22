# list all targets and exit
default: 
    just --list

# run locally using docker-compose
up *flags="": 
    docker compose up --build {{flags}}

# list all targets and exit
default: 
    just --list

# run api
run:
    poetry run fastapi dev app/main.py

# run locally using docker-compose
up *flags="": 
    docker compose up --build {{flags}}

# format python code
format:
    poetry run isort .
    poetry run black .

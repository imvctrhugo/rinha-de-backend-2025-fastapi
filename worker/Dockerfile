FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN rm -rf /var/lib/apt/lists/*

# Install & configure poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry

# Install dependencies with poetry (excluding dev dependencies)
COPY pyproject.toml poetry.lock  ./
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Copy the rest of the application code into the container at /
COPY . .

# Command to run the application using uvicorn
CMD ["python", "app/main.py"]

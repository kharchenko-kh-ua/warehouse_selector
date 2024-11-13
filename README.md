# FastAPI Application Example

This is a sample project built using FastAPI. The project demonstrates a python web application with database interactions,
API endpoint and automated testing.

## Overview

This application uses endpoint for managing and selecting optimal warehouse configurations based on dynamic data from a PostgreSQL database.
This example also includes unit tests and a CI/CD pipeline configuration to ensure code quality and deployment readiness.

## Technologies Used

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Docker & Docker Compose**
- **GitHub Actions**
- **Pre-commit**
- **Pipenv**

### Linters & Formatters:
- **black**
- **ruff**
- **mypy**
- **pylint**
- **isort**

## Getting Started

### Prerequisites

- **Docker**: Make sure Docker is installed and running.
- **Pipenv**: Ensure Pipenv is installed for managing dependencies.

### Running the Application

1. Clone the repository:

    ```bash
    git clone git@github.com:kharchenko-kh-ua/warehouse_selector.git
    cd warehouse_selector
    ```

2. Install dependencies:

    ```bash
    pipenv install --dev
    ```

3. Run the Docker Compose setup: This will start the FastAPI application and PostgreSQL database services.

    ```bash
    docker-compose up --build
    ```

4. Apply database migrations: Inside the FastAPI container, apply migrations using Alembic to set up the database schema.

    ```bash
    docker-compose exec app alembic upgrade head
    ```

5. Access the API: The application should now be running on [http://localhost:8000](http://localhost:8000).

    Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive API documentation.

### Running Unit Tests

Unit tests are located in the `tests/` directory and can be run with `pytest`.

1. Ensure services are running in docker:

    ```bash
    docker exec -it $(docker ps -aqf name="web-1") pytest
    ```


### Using Pre-commit Hooks

Pre-commit hooks are configured to automatically run linters and formatters when code is committed. To enable pre-commit hooks:

1. Install pre-commit:

    ```bash
    pip install pre-commit
    ```

2. Set up hooks:

    ```bash
    pre-commit install
    ```

3. Run pre-commit hooks manually (optional):

    ```bash
    pre-commit run --all-files
    ```

## CI/CD Pipeline with GitHub Actions

The project includes a GitHub Actions configuration file `.github/workflows/ci.yml` to automate testing and code quality checks.

The pipeline will:

- Install dependencies
- Run linters and formatters (black, ruff, pylint)
- Run type checking with mypy
- Execute unit tests with pytest

The pipeline is configured to run on all branches upon any push or pull_request event.

## Additional Notes

- **Database Configuration**: You can configure the database connection by modifying the `DATABASE_URL` in the `.env` file.
- **Docker Compose**: The `docker-compose.yaml` file contains the configuration for the application and database services. Ensure the `docker-compose up --build` command is run from the root directory.

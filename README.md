# Redirect Service

## Introduction

This repository contains the source code for a FastAPI-based redirect service. The service is designed to efficiently redirect incoming HTTP requests to various destinations based on pre-defined rules, while preserving URL parameters and structure.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Docker
- Poetry for Python package management

### Installing for Development

To set up the development environment, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Run the following command to install dependencies:

```bash
make dev
```

This command will install Poetry (if not already installed) and use it to install the required Python packages.

### Running Tests

To run tests, execute the following command in the project's root directory:

```bash
make test
```

This command will use Poetry to run tests with pytest.

### Running the Service

To run the service using Docker, you can use the Makefile as follows:

```bash
make run
```

This command performs the following actions:

- Stops any existing Docker container with the name redirect-service-container.
- Removes the stopped container.
- Builds a Docker image named redirect-service.
- Runs a new container with the name redirect-service-container, mapping port 80 of the container to port 80 of the host machine.

### Deployment

The service is containerized using Docker, allowing for easy deployment in various environments. 
The `make run` command can be used for local deployment and testing.
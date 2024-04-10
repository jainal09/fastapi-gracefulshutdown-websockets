# Fast Api Graceful Shutdowns with Websockets

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Dependency Management: Poetry](https://img.shields.io/badge/Dependency%20Managment-Poetry-blue?logo=python&logoColor=yellow)](https://python-poetry.org/) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
 [![Linter: Flake8](https://img.shields.io/badge/Linter-Flake8-blue?logo=python&logoColor=yellow)](https://flake8.pycqa.org/en/latest/) [![Formatter: Black](https://img.shields.io/badge/Formatter-Black-blue?logo=python&logoColor=yellow)](https://black.readthedocs.io/en/stable/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![python: 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

![Header Image](images/header.png)

This project demonstrates how to implement graceful shutdowns using FastAPI and kubernetes,
that uses websockets client connections and internal background queues.

## Blog Post
I have written a blog post on this project. You can read it [here](https://www.linkedin.com/pulse/gracefully-implementing-graceful-shutdowns-jainal-gosaliya-pps5e/). In this blog post, I have explained the importance of graceful shutdowns and how to implement them in FastAPI with websockets.

## Overview

When deploying a new version of an application, it is essential to ensure that no tasks are lost during the deployment process. This is especially important for applications that use websockets to maintain real-time connections with clients. In such cases, abruptly terminating the application can lead to data loss and client disconnections.

## Solution

Here we have a FastAPI server, deployed in a pod of Kubernetes with min-replicas set to 1 for simplicity. It has a rest API to send tasks, a WebSocket interface for sending task status events to the clients, and a signal listener that listens to pod termination signals sent by Kubernetes.
Through the rest API, a task is created and enqueued to the inbuilt fast-api background queue and is later processed by the worker. Once, the task is processed the client is notified via WebSocket.
The custom-implemented signal listener listens to all the SIGTERM signals send by the Kubernetes controller when a pod termination happens. This is the watcher that steers the entire graceful shutdown part.

## Features

✅ Ensure zero task loss during deployments
🔗 Keep existing clients connected while preventing new connections to a terminating pod
📣 Provide real-time feedback to clients through WebSocket notifications
🚦 Mitigate race conditions between pod termination and task creation

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/jainal09/fastapi-gracefulshutdown-websockets.git
    ```

2. Install the dependencies:
   
   > You will need [poetry](https://python-poetry.org/) to install the project dependencies.

   ```shell
   poetry install --no-dev # for production
   # or
   poetry install # for development
   ```
## Usage


1. Start the FastAPI application:

    ```shell
    python main.py
    ```

2. Open your web browser and navigate to `http://localhost:8000/docs` to access the 
   application.

### Kubernetes
1. Deploy the application to a Kubernetes cluster:

    ```shell
    kubectl apply -f k8s/deployment.yaml
    ```
2. Access the application at `http://localhost:30000/docs`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements,
please open an issue or submit a pull request.

## Linting and Formatting
1. Lint the code using ruff:
    
    ```shell
    ruff check --fix .
    ```
## Type Checking
1. Run the type checker:

    ```shell
    mypy .
    ```

## Docker
1. Image available on Docker Hub: [jainal09/grs-fast-api](https://hub.docker.com/repository/docker/jainal09/grs-fast-api/general)

2. Build the Docker imag locally:

```shell
docker build -t jainal09/grs-fast-api:v9 .
```

## License

This project is licensed under the [MIT License](LICENSE).

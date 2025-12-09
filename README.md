# LLM Inference Microservice

A production-ready, containerized REST API for serving Large Language Models (LLMs). This service is built with FastAPI and utilizes `distilgpt2` for efficient CPU-based inference.

## Features

* **Scalable API:** Built on FastAPI with asynchronous request handling.
* **Concurrency Managed:** Heavy model inference is offloaded to thread pools (`run_in_threadpool`) to keep the server responsive.
* **Resource Optimized:** Uses a Singleton pattern for lazy model loading and CPU-optimized PyTorch builds to minimize image size and memory usage.
* **Secure:** Endpoint protection using API Key authentication via environment variables.
* **Containerized:** Fully Dockerized with resource limits and non-root user security.

## Prerequisites

* Docker
* Docker Compose

## Quick Start

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd llm-api-service
    ```

2.  **Start the service:**
    Run the following command to build and start the container. The first run may take a few minutes to download the model and dependencies.
    ```bash
    docker-compose up --build
    ```

3.  **Verify Status:**
    Visit `http://localhost:8000/health` to see if the service is running.

## API Documentation

### 1. Health Check
* **Endpoint:** `GET /health`
* **Description:** Returns the service status to verify availability.
* **Response:**
    ```json
    {
      "status": "ok",
      "service": "LLM-Generator"
    }
    ```

### 2. Generate Text
* **Endpoint:** `POST /generate`
* **Description:** Accepts a text prompt and generates a continuation using the LLM.
* **Headers:**
    * `x-api-key`: `gpp-llm-service-secret` (Configured in `docker-compose.yml`).
* **Request Body (JSON):**
    ```json
    {
      "prompt": "The future of AI is",
      "max_new_tokens": 50
    }
    ```
    * `prompt`: (Required) The input text string.
    * `max_new_tokens`: (Optional) Maximum number of tokens to generate (Default: 50, Max: 200).

* **Success Response (200 OK):**
    ```json
    {
      "generated_text": "The future of AI is promising because..."
    }
    ```

* **Error Response (401 Unauthorized):**
    Occurs if the `x-api-key` header is missing or incorrect.

### Interactive Documentation
Once the application is running, you can access the auto-generated Swagger UI to test endpoints interactively:
* **URL:** `http://localhost:8000/docs`

## Architecture & Design Choices

### Singleton Model Loading
To prevent memory bloat and slow startup times, the LLM (`distilgpt2`) is implemented as a **Singleton** via the `LLMEngine` class. It uses "lazy loading," meaning the model is loaded into memory only when the first request is received.

### Concurrency Handling
LLM inference is a CPU-bound operation. If run directly on the main asyncio event loop, it would block the server, causing other requests (like health checks) to hang.
* **Solution:** We use `fastapi.concurrency.run_in_threadpool` to execute the inference in a separate thread, ensuring the main application loop remains non-blocking.

### Docker Optimization
* **Base Image:** We use `python:3.10-slim` to keep the footprint small.
* **CPU-Only PyTorch:** The build explicitly installs the CPU version of PyTorch (`--index-url https://download.pytorch.org/whl/cpu`) to save significant disk space (~2GB) compared to the GPU version.
* **Security:** The application runs as a non-root user (`appuser`) inside the container.

## Configuration

The service is configured via environment variables defined in `docker-compose.yml`:

| Variable | Value | Description |
| :--- | :--- | :--- |
| `API_KEY` | `gpp-llm-service-secret` | The secret key required for the `x-api-key` header. |
| `TRANSFORMERS_CACHE` | `/tmp/transformers_cache` | Path for caching downloaded models. |
# Flower Monitoring Guide

This guide explains how to use the Flower monitoring extension with your
Celery worker deployment.

## What is Flower?

Flower is a real-time monitoring and administration dashboard for Celery.
It provides:

- **Real-time stats**: Live metrics on task processing rates, queue depths,
  and worker utilization.
- **Task details**: Inspect individual task status, arguments, results, and
  timing information.
- **Worker management**: View worker status, configured queues, and active
  tasks. Restart or shut down workers remotely.
- **Events**: Capture and display real-time events from workers.

## Prerequisites

- A running Celery worker with a Redis broker
- The `celery-docker` extension installed (for Docker Compose)
- Docker available on your machine

## Setup

1. Scaffold a project with the Flower extension:

   ```sh
   uvx create-awesome-python-app my-worker \
     --template celery-worker \
     --addons celery-docker flower-docker \
     --yes
   ```

2. Populate your `.env` file:

   ```bash
   # Required
   BROKER_URL=redis://redis:6379/0

   # Flower settings (optional, defaults shown)
   FLOWER_PORT=5555
   FLOWER_HOST=0.0.0.0

   # Optional: HTTP basic auth
   # FLOWER_BASIC_PASSWORD=your_secret_password
   ```

3. Start the services:

   ```sh
   docker compose up --build
   ```

4. Open the dashboard at `http://localhost:5555`.

## Security considerations

- **Never commit `.env` files** to version control. Add `.env` to
  `.gitignore`.
- Flower can expose task arguments and results. If you are processing
  sensitive data, enable HTTP basic auth with `FLOWER_BASIC_PASSWORD`.
- In production, consider placing Flower behind a reverse proxy with TLS.

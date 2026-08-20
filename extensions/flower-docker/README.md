# Flower Monitoring Extension for Celery

Adds Flower monitoring dashboard for Celery workers.

## Features

- **Flower Integration**: Provides a Flask-based monitoring dashboard for Celery workers
- **Real-time Metrics**: Live stats on task queues, worker performance, and task execution
- **Docker Compose Support**: Includes a dedicated `flower` service in the compose configuration
- **Environment Variables**: Secrets (Redis URLs, Flower port) are loaded from `.env` files only

## Installation

```sh
uvx create-awesome-python-app my-worker \
  --template celery-worker \
  --addons flower-docker \
  --yes
```

## Configuration

The extension requires:
- `FLOWER_PORT` (default: 5555) - Port for the Flower dashboard
- `FLOWER_HOST` (default: "0.0.0.0") - Host to bind the Flower server
- `REDIS_URL` - Redis connection string (must match celery worker config)

## Usage

1. Start the worker with the flower-docker addon:
   ```sh
   uvx create-awesome-python-app my-worker \
     --template celery-worker \
     --addons flower-docker \
     --yes
   ```

2. Access the Flower dashboard at `http://localhost:5555`

3. Configure `FLOWER_PORT` and `FLOWER_HOST` in your `.env` file.

## Requirements

- Python 3.12+
- Celery (>=5.0)
- Flower (>=2.0)
- Redis (for broker)

## Security

- All secrets (Redis URLs, Flower port) are loaded from environment variables only
- No hardcoded credentials in source code
- Follows the same security patterns as the celery-docker extension

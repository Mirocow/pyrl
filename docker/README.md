# Pyrl Docker Services

Docker configurations for running Pyrl language platform in containerized environments.

## Quick Start

```bash
# Start main API server
docker-compose up -d server

# Start interactive console
docker-compose run console

# Start development environment
docker-compose --profile dev up -d dev
```

## Available Services

### 1. Server (`pyrl-server`)
Main API server for Pyrl language execution.

- **Port**: 8000
- **Dockerfile**: `Dockerfile.server`
- **Usage**:
  ```bash
  docker-compose up -d server
  curl http://localhost:8000/health
  ```

### 2. Console (`pyrl-console`)
Interactive Pyrl REPL console.

- **Dockerfile**: `Dockerfile.console`
- **Usage**:
  ```bash
  docker-compose run console
  ```

### 3. Development (`pyrl-dev`)
Full development environment with hot-reload.

- **Ports**: 8000 (API), 8888 (Jupyter)
- **Dockerfile**: `Dockerfile.dev`
- **Usage**:
  ```bash
  docker-compose --profile dev up -d dev
  docker exec -it pyrl-dev bash
  ```

## Training Services (GPU Required)

### 4. Model Generator (`pyrl-model-generator`)
Generates trained Pyrl language models.

- **Dockerfile**: `Dockerfile.model-generator`
- **Usage**:
  ```bash
  docker-compose --profile training run model-generator
  ```

### 5. Training (`pyrl-training`)
Full model training pipeline.

- **Dockerfile**: `Dockerfile.training`
- **Volumes**: checkpoints, logs, output
- **Usage**:
  ```bash
  docker-compose --profile training up -d training
  ```

### 6. Model Inference (`pyrl-model-inference`)
GPU-accelerated model inference server.

- **Port**: 8001
- **Dockerfile**: `Dockerfile.model-inference`
- **Requires**: NVIDIA GPU with nvidia-docker
- **Usage**:
  ```bash
  docker-compose --profile inference up -d model-inference
  ```

## Volumes

| Volume | Description |
|--------|-------------|
| `console-history` | REPL command history |
| `training-checkpoints` | Model training checkpoints |
| `training-logs` | Training logs |
| `training-output` | Trained model outputs |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYRL_DEBUG` | `false` | Enable debug mode |
| `PYRL_SERVER_HOST` | `0.0.0.0` | Server host |
| `PYRL_SERVER_PORT` | `8000` | Server port |
| `PYRL_DATA_DIR` | `/app/data` | Data directory |
| `PYRL_MODELS_DIR` | `/app/models` | Models directory |
| `WANDB_API_KEY` | - | Weights & Biases API key |

## GPU Support

For training and inference services, ensure you have:

1. NVIDIA GPU with CUDA support
2. [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) installed
3. Updated NVIDIA drivers

Verify GPU access:
```bash
docker run --gpus all nvidia/cuda:11.8-base nvidia-smi
```

## Building Individual Images

```bash
# Build server image
docker build -f docker/Dockerfile.server -t pyrl-server .

# Build training image
docker build -f docker/Dockerfile.training -t pyrl-training .

# Build all images
docker-compose build
```

## Production Deployment

For production use:

1. Use the server image only
2. Configure proper volume mounts
3. Set up reverse proxy (nginx/traefik)
4. Enable HTTPS
5. Configure resource limits

Example production compose:
```yaml
services:
  server:
    image: pyrl-server:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - PYRL_DEBUG=false
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    restart: always
```

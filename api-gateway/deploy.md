To build and push **both** the API Gateway and the Executor images to Docker Hub, you can target each specific Dockerfile using the `-f` flag.

Run the following commands from your project root:

### 1. Build and Push the API Gateway

```bash
docker build -t 2000023946/orion-api:latest -f dockerfile .
docker push 2000023946/orion-api:latest

```

### 2. Build and Push the Executor

```bash
docker build -t 2000023946/orion-executor:latest -f dockerfile.executor .
docker push 2000023946/orion-executor:latest

```

### 3. Restart Your Kubernetes Deployments

Once both images are pushed, roll out the updates in your cluster so Kubernetes pulls the latest versions:

```bash
kubectl rollout restart deployment api-gateway
kubectl rollout restart deployment orion-executor
```
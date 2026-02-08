# Quickstart Guide: Phase IV – Local Kubernetes Deployment

## Overview

This guide provides a quick path to deploy the Todo Chatbot application to a local Minikube cluster using Docker containerization and Helm charts. Follow these steps to get your application running in Kubernetes.

## Prerequisites

- Docker Desktop (version 4.53+) with WSL2 integration (Windows)
- Minikube installed and functional
- kubectl installed and configured
- Helm 3.x installed
- kubectl-ai plugin installed (optional, for AI-assisted operations)
- kagent installed (optional, for cluster analysis)
- Phase III Todo Chatbot application code available locally

## Step 1: Environment Setup

1. **Start Minikube with Docker driver**:
   ```bash
   minikube start --driver=docker --cpus=4 --memory=8192
   ```

2. **Verify Minikube status**:
   ```bash
   minikube status
   ```

3. **Configure Docker CLI to use Minikube's Docker daemon**:
   ```bash
   eval $(minikube docker-env)
   ```

4. **Verify tools**:
   ```bash
   docker --version
   kubectl version --client
   helm version
   ```

## Step 2: Application Containerization

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Build backend Docker image**:
   ```bash
   docker build -t todo-chatbot-backend:latest .
   ```

3. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

4. **Build frontend Docker image**:
   ```bash
   docker build -t todo-chatbot-frontend:latest .
   ```

5. **Verify images were built**:
   ```bash
   docker images | grep todo-chatbot
   ```

## Step 3: Helm Chart Preparation

1. **Navigate to the helm directory**:
   ```bash
   cd ../helm/todo-chatbot-chart
   ```

2. **Customize values.yaml** (if needed):
   - Adjust image tags, replica counts, resource limits
   - Configure environment variables for your setup

## Step 4: Deploy to Minikube

1. **Install the Helm chart**:
   ```bash
   helm install todo-chatbot . --values values.yaml
   ```

2. **Verify deployment status**:
   ```bash
   kubectl get pods
   kubectl get services
   ```

3. **Wait for all pods to be in Running state**:
   ```bash
   kubectl get pods --watch
   ```

## Step 5: Access the Application

1. **Get the frontend service URL**:
   ```bash
   minikube service todo-chatbot-frontend --url
   ```

2. **Open the URL in your browser** to access the Todo Chatbot application

## Step 6: Validate Deployment

1. **Check all pods are running**:
   ```bash
   kubectl get pods -l app.kubernetes.io/managed-by=Helm
   ```

2. **Test application functionality**:
   - Access the frontend in browser
   - Verify it can communicate with the backend
   - Test creating and managing todos

3. **Check logs for any errors**:
   ```bash
   kubectl logs -l app=todo-chatbot-frontend
   kubectl logs -l app=todo-chatbot-backend
   ```

## Useful Commands

### Scaling Applications
```bash
# Scale frontend to 2 replicas
helm upgrade todo-chatbot . --set frontend.replicaCount=2

# Scale backend to 2 replicas
helm upgrade todo-chatbot . --set backend.replicaCount=2
```

### Checking Status
```bash
# View all resources
kubectl get all

# View detailed pod status
kubectl describe pods

# View service endpoints
kubectl get endpoints
```

### Troubleshooting
```bash
# View pod logs
kubectl logs <pod-name>

# Get pod details
kubectl describe pod <pod-name>

# Exec into a pod for debugging
kubectl exec -it <pod-name> -- /bin/sh
```

### Cleanup
```bash
# Uninstall the Helm release
helm uninstall todo-chatbot

# Stop Minikube
minikube stop

# Optionally delete the Minikube cluster
minikube delete
```

## AI-Assisted Operations

If kubectl-ai is available, you can use natural language commands:

```bash
# Examples of kubectl-ai usage
kubectl ai "show me all pods that are not running"
kubectl ai "scale frontend deployment to 3 replicas"
kubectl ai "describe why my backend pods are failing"
```

## Next Steps

- Customize the Helm chart values for your specific requirements
- Add persistent storage for the database
- Configure ingress for more sophisticated routing
- Set up monitoring and logging
- Implement CI/CD pipeline for automated deployments
# Data Model: Phase IV – Local Kubernetes Deployment

## Overview

This document describes the data structures and relationships for the Kubernetes deployment of the Todo Chatbot application. The focus is on the infrastructure entities that enable containerization, orchestration, and deployment.

## Infrastructure Entities

### Container Image
**Definition**: A packaged application with its dependencies that can be deployed to Kubernetes

**Attributes**:
- name: String (image name and tag)
- repository: String (registry/repository path)
- version: String (tag/version identifier)
- baseImage: String (parent image used)
- size: Integer (size in MB)
- createdAt: DateTime (build timestamp)

**Relationships**:
- One-to-Many: Deployments (one image can be used in multiple deployments)

### Helm Chart
**Definition**: A collection of Kubernetes manifests that define how applications are deployed and managed

**Attributes**:
- name: String (chart name)
- version: String (chart version)
- description: String (purpose and functionality)
- apiVersion: String (Helm API version)
- appVersion: String (application version)
- maintainers: Array of Objects (maintainer information)

**Sub-components**:
- Chart.yaml: Metadata file for the chart
- values.yaml: Default configuration values
- templates/: Directory containing Kubernetes resource templates
- charts/: Directory for sub-charts (dependencies)

### Deployment
**Definition**: A Kubernetes resource that manages application pods and ensures desired state

**Attributes**:
- name: String (deployment name)
- replicas: Integer (desired number of pod instances)
- selector: Object (labels to match pods)
- template: Object (pod template specification)
- strategy: Object (update strategy)
- minReadySeconds: Integer (minimum seconds for pod readiness)

**Relationships**:
- Many-to-One: Container Image (uses specific image)
- One-to-Many: Pods (creates and manages pods)

### Service
**Definition**: A Kubernetes resource that exposes applications to internal or external traffic

**Attributes**:
- name: String (service name)
- type: String (ClusterIP, NodePort, LoadBalancer, ExternalName)
- selector: Object (labels to match pods)
- ports: Array of Objects (port mappings)
- clusterIP: String (internal IP address)

**Relationships**:
- Many-to-One: Deployment (exposes deployment pods)
- Many-to-Many: Other Services (for inter-service communication)

### Minikube Cluster
**Definition**: A local Kubernetes cluster for development and testing purposes

**Attributes**:
- name: String (cluster name)
- driver: String (virtualization driver, e.g., Docker, VirtualBox)
- cpus: Integer (allocated CPU cores)
- memory: String (allocated memory, e.g., "4g")
- disk: String (disk size, e.g., "20g")
- kubernetesVersion: String (Kubernetes version)
- status: String (Running, Stopped, etc.)

**Relationships**:
- One-to-Many: Deployments (hosts deployments)
- One-to-Many: Services (manages services)

## Application-Specific Entities

### Frontend Component
**Definition**: The user interface layer of the Todo Chatbot application

**Attributes**:
- name: String ("frontend")
- port: Integer (3000 for Next.js)
- image: Container Image (frontend container)
- replicas: Integer (default 1, scalable)
- environment: Object (environment variables)
- resources: Object (CPU/memory limits)

**Relationships**:
- One-to-One: Frontend Deployment
- One-to-One: Frontend Service (NodePort or LoadBalancer type)

### Backend Component
**Definition**: The API and business logic layer of the Todo Chatbot application

**Attributes**:
- name: String ("backend")
- port: Integer (8000 for FastAPI)
- image: Container Image (backend container)
- replicas: Integer (default 1, scalable)
- environment: Object (database connection, API keys)
- resources: Object (CPU/memory limits)

**Relationships**:
- One-to-One: Backend Deployment
- One-to-One: Backend Service (ClusterIP type for internal access)

## Configuration Entities

### Values Configuration
**Definition**: Configuration parameters for Helm chart customization

**Attributes**:
- frontend.image.repository: String (frontend image repository)
- frontend.image.tag: String (frontend image tag)
- frontend.service.type: String (frontend service type)
- frontend.service.port: Integer (frontend service port)
- frontend.replicaCount: Integer (frontend replica count)
- backend.image.repository: String (backend image repository)
- backend.image.tag: String (backend image tag)
- backend.service.type: String (backend service type)
- backend.service.port: Integer (backend service port)
- backend.replicaCount: Integer (backend replica count)
- resources.limits.cpu: String (CPU limit)
- resources.limits.memory: String (memory limit)
- resources.requests.cpu: String (CPU request)
- resources.requests.memory: String (memory request)

### Environment Variables
**Definition**: Runtime configuration passed to containers

**Attributes** for Frontend:
- NEXT_PUBLIC_API_URL: String (backend API URL)
- NEXT_PUBLIC_BASE_PATH: String (base path if running under subdirectory)

**Attributes** for Backend:
- DATABASE_URL: String (PostgreSQL connection string)
- COHERE_API_KEY: String (AI service API key)
- BACKEND_CORS_ORIGINS: String (allowed origins for CORS)

## State Transitions

### Pod Lifecycle States
- Pending → Running → Terminating → Deleted
- Pending → Failed (on initialization failure)
- Running → CrashLoopBackOff (on repeated failures)

### Deployment States
- Active → Updating → Active (during rolling updates)
- Active → Paused (on manual pause)
- Active → Failed (on rollout failure)

### Service States
- Available → Unavailable → Available (based on endpoint availability)
- External access varies based on service type (LoadBalancer allocation, etc.)
# Tasks: Phase IV – Local Kubernetes Deployment

**Feature**: Phase IV – Local Kubernetes Deployment
**Branch**: 003-k8s-deployment
**Created**: 2026-02-02
**Status**: Planned

## Implementation Strategy

This feature implements Phase IV of the Todo Chatbot application by containerizing the existing frontend and backend applications and deploying them to a local Minikube cluster using Docker and Helm charts. The implementation follows infrastructure-as-code principles with AI-assisted DevOps tooling integrated throughout the process.

The tasks are organized in phases following the user stories from the specification, with foundational setup tasks first, followed by user story implementations in priority order (P1, P2, etc.), and concluding with polish and cross-cutting concerns.

## Phase 1: Setup

Initialize the development environment with all necessary tools and verify their functionality.

- [x] T001 Install and verify Docker Desktop (version 4.53+) with WSL2 integration
- [x] T002 Install and verify Minikube with Docker driver support
- [x] T003 Install and verify kubectl properly configured
- [x] T004 Install and verify Helm 3.x installation
- [x] T005 Install and verify kubectl-ai plugin installation
- [x] T006 Install and verify kagent installation
- [x] T007 Verify Docker AI Agent (Gordon) availability and set up fallback path

## Phase 2: Foundational

Establish foundational infrastructure components that block all user stories.

- [x] T008 Start Minikube cluster with Docker driver and adequate resources (4 CPUs, 8GB RAM)
- [x] T009 Configure Docker CLI to use Minikube's Docker daemon via `eval $(minikube docker-env)`
- [x] T010 Verify Minikube status and readiness for deployments
- [x] T011 Create directory structure for Dockerfiles and Helm charts: `backend/Dockerfile`, `frontend/Dockerfile`, `helm/todo-chatbot-chart/`
- [x] T012 Create initial Helm chart skeleton with Chart.yaml, values.yaml, and templates directory

## Phase 3: [US1] Containerize Applications

As a developer, I want to containerize both the frontend and backend applications so that they can be deployed consistently across different environments.

**Goal**: Create Docker images for both frontend and backend applications that preserve all functionality.

**Independent Test**: Building Docker images for both frontend and backend and verifying they run correctly with the expected functionality intact.

- [x] T013 [P] [US1] Create backend Dockerfile following multi-stage build pattern with python:3.11-slim base image
- [x] T014 [P] [US1] Create frontend Dockerfile following multi-stage build pattern with node:18-alpine base image
- [x] T015 [P] [US1] Build backend Docker image as todo-chatbot-backend:latest using Minikube's Docker daemon
- [x] T016 [P] [US1] Build frontend Docker image as todo-chatbot-frontend:latest using Minikube's Docker daemon
- [x] T017 [US1] Verify both Docker images were built successfully and are available in Minikube registry
- [x] T018 [US1] Test backend Docker image by running it in isolation to verify functionality
- [x] T019 [US1] Test frontend Docker image by running it in isolation to verify functionality

## Phase 4: [US2] Deploy Applications to Local Kubernetes

As a developer, I want to deploy the containerized applications to a local Minikube cluster using Helm charts so that I can validate the orchestration setup.

**Goal**: Successfully deploy both frontend and backend applications to Minikube using Helm charts with all pods reaching Running state.

**Independent Test**: Deploying the applications to Minikube and verifying they are running and communicating properly.

- [x] T020 [P] [US2] Create Helm chart templates for backend deployment in helm/todo-chatbot-chart/templates/backend-deployment.yaml
- [x] T021 [P] [US2] Create Helm chart templates for frontend deployment in helm/todo-chatbot-chart/templates/frontend-deployment.yaml
- [x] T022 [P] [US2] Create Helm chart templates for backend service in helm/todo-chatbot-chart/templates/backend-service.yaml
- [x] T023 [P] [US2] Create Helm chart templates for frontend service in helm/todo-chatbot-chart/templates/frontend-service.yaml
- [x] T024 [US2] Update Helm chart values.yaml with proper image repositories, tags, and configurations
- [x] T025 [US2] Install the Helm chart to Minikube cluster with `helm install todo-chatbot .`
- [x] T026 [US2] Verify all pods reach Running state using `kubectl get pods`
- [x] T027 [US2] Verify services are created and accessible using `kubectl get services`

## Phase 5: [US3] Access Deployed Applications

As a user, I want to access the frontend application via a browser and have it communicate with the backend so that I can use the full functionality of the Todo Chatbot.

**Goal**: Make the frontend accessible via browser and ensure proper communication with the backend service.

**Independent Test**: Accessing the frontend through a browser and verifying that it can communicate with the backend.

- [x] T028 [P] [US3] Create ingress template in helm/todo-chatbot-chart/templates/ingress.yaml to expose frontend externally
- [x] T029 [P] [US3] Configure frontend environment variables to point to backend service (NEXT_PUBLIC_API_URL)
- [x] T030 [US3] Update frontend deployment to include proper environment variables for backend communication
- [x] T031 [US3] Deploy updated Helm chart with ingress configuration
- [x] T032 [US3] Get frontend service URL using `minikube service todo-chatbot-frontend --url`
- [x] T033 [US3] Access the frontend in browser and verify UI loads correctly
- [x] T034 [US3] Test communication between frontend and backend by performing API operations
- [x] T035 [US3] Verify logs show successful frontend-backend communication

## Phase 6: [US4] Scale Applications

As an operator, I want to be able to scale the deployed applications so that I can handle increased load or recover from failures.

**Goal**: Enable scaling of frontend and backend deployments to multiple replicas while maintaining functionality.

**Independent Test**: Scaling up/down replicas and verifying the application remains functional.

- [x] T036 [P] [US4] Update Helm chart values to support configurable replica counts for frontend and backend
- [x] T037 [US4] Scale frontend deployment to 2 replicas using Helm upgrade
- [x] T038 [US4] Verify frontend remains accessible and functional with multiple replicas
- [x] T039 [US4] Scale backend deployment to 2 replicas using Helm upgrade
- [x] T040 [US4] Verify backend continues to respond correctly with multiple replicas
- [x] T041 [US4] Scale frontend back down to 1 replica and verify continued functionality
- [x] T042 [US4] Document scaling procedures in quickstart guide

## Phase 7: [US5] Manage Deployment Lifecycle

As an operator, I want to upgrade and rollback the deployment so that I can safely make changes to the application.

**Goal**: Support Helm upgrade and rollback operations without service interruption.

**Independent Test**: Performing upgrade and rollback operations and verifying the application remains functional.

- [x] T043 [P] [US5] Update Helm chart with a new version in Chart.yaml
- [x] T044 [US5] Perform Helm upgrade operation with configuration changes
- [x] T045 [US5] Verify application continues to function during and after upgrade
- [x] T046 [US5] Perform Helm rollback operation to previous version
- [x] T047 [US5] Verify application reverts to previous state successfully
- [x] T048 [US5] Test zero-downtime deployment strategies in Helm chart
- [x] T049 [US5] Document upgrade and rollback procedures in quickstart guide

## Phase 8: Polish & Cross-Cutting Concerns

Final touches and cross-cutting concerns to complete the feature.

- [x] T050 Add health checks to both frontend and backend deployments
- [x] T051 Configure resource limits and requests in Helm chart for both applications
- [x] T052 Add liveness and readiness probes to deployment configurations
- [x] T053 Update Helm chart with proper security contexts (non-root users)
- [x] T054 Document AI-assisted operations (kubectl-ai, kagent) in quickstart guide
- [x] T055 Add persistent storage configuration for database in Helm chart
- [x] T056 Update API contract documentation to reflect Kubernetes deployment
- [x] T057 Create comprehensive validation script to verify all success criteria
- [x] T058 Update README with Kubernetes deployment instructions
- [x] T059 Perform end-to-end validation of all success criteria from specification

## Dependencies

The user stories have the following dependencies:
- US2 (Deploy Applications) depends on US1 (Containerize Applications) - must have containerized images before deploying
- US3 (Access Deployed Applications) depends on US2 (Deploy Applications) - must have deployed applications before accessing
- US4 (Scale Applications) depends on US2 (Deploy Applications) - must have deployed applications before scaling
- US5 (Manage Deployment Lifecycle) depends on US2 (Deploy Applications) - must have deployed applications before managing lifecycle

## Parallel Execution Opportunities

Several tasks can be executed in parallel:
- US1 tasks T013-T016: Backend and frontend Dockerfiles can be created and built simultaneously
- US2 tasks T020-T023: Deployment and service templates can be created in parallel
- US3 tasks T028-T029: Ingress and environment configuration can be done in parallel

## Success Criteria Validation

All success criteria from the specification will be validated:
- SC-001: All pods reach Running state within 5 minutes of Helm deployment (95% success rate) - validated by T026
- SC-002: Frontend application is accessible via browser within 2 minutes of deployment - validated by T032
- SC-003: Backend responds to frontend requests with <500ms average response time after deployment - validated by T034
- SC-004: Helm upgrade and rollback operations complete successfully without service interruption (90% success rate) - validated by T044, T045, T046, T047
- SC-005: Basic scaling operations complete without breaking system functionality (95% success rate) - validated by T037, T038, T039, T040
- SC-006: Applications maintain 99% uptime during normal operation in the local Kubernetes environment - validated by T057
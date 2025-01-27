# Kubernetes Health Check with Kafka Integration  

This project provides a comprehensive system to monitor the health of all pods in a Kubernetes cluster, send their status to a Kafka pool, and expose this data through a REST API.  

## Features  

- **Health Check Service**: Periodically checks the status of all Kubernetes pods and publishes the results to a Kafka topic.  
- **Consumer Health Check Service**: A REST API that consumes messages from Kafka and returns pod statuses in its responses.  
- **Monitoring**: Prometheus and Grafana services are deployed for monitoring metrics and visualizing data.  

## Prerequisites  

Ensure the following are installed on your system:  
- [Python 3.x](https://www.python.org/downloads/)  
- [Terraform](https://www.terraform.io/downloads.html)  
- [Docker](https://www.docker.com/products/docker-desktop)  
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)  

## Setup  

Follow these steps to set up and run the project:  

### 1. Clone the Repository  

```bash  
git clone <repository-url>  
cd <repository-folder>  
```

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 2.1 Install Minikube
![[https://github.com/health-check/public/Screenshot2025-01-27at13.33.38.png]]

#### 2.2 Build Docker image
```
docker build -t MyImage .
```
![[Shttps://github.com/health-check/public/Screenshot2025-01-27at13.58.12.png]]
#### 3. Apply Terraform Plan

#### 3. Apply Terraform Plan
```
terraform init
terraform plan
terraform apply
```
![[https://github.com/health-check/public/Screenshot2025-01-27at13.34.16.png]]
![[https://github.com/health-check/public/Screenshot2025-01-27at13.36.07.png]]
This will provision:

- Kafka cluster
- Prometheus and Grafana monitoring services
- Kubernetes deployments for the health check services

#### Health Check Service

This service runs periodically to check pod statuses and publish them to Kafka. It is deployed as part of the Kubernetes setup.

#### Consumer Health Check Service

This REST API provides pod status information by consuming messages from Kafka. You can access the API after deployment.

#### Monitoring Services

- **Prometheus**: Use the Prometheus UI for metrics monitoring.
- **Grafana**: Pre-configured dashboards to visualize the health of your Kubernetes cluster.

#### Check all resources that had been deployed
```
kubectl get all -n MyNamespace
```
![[https://github.com/health-check/public/Screenshot2025-01-27at13.37.57.png]]
### 6. API Details

#### `Consumer Health Check Service` API

##### Endpoint: `/check_health`

- **Method**: GET
- **Response**:
```json
[ { "serviceName": "example-service", "status": "Running", "timestamp": "2025-01-27T12:00:00Z" }, { "serviceName": "another-service", "status": "Pending", "timestamp": "2025-01-27T12:00:00Z" } ]
```

![[https://github.com/health-check/public/Screenshot2025-01-27at13.45.16.png]]

### 7. Monitoring Access

- **Prometheus**: Open the Prometheus dashboard using Minikube:
```bash
minikube service prometheus-service
```

- **Grafana**: Open the Grafana dashboard using Minikube:
```bash
minikube service grafana-service
```    

```
kubectl port-forward -n $MY_NAMESPACE services/prometheus-stack-grafana -p 3000:3000
```

![[https://github.com/health-check/public/Screenshot2025-01-27at13.47.36.png]]

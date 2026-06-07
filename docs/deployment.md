# Arogya Deployment Guide

This guide describes how to deploy the Arogya medical research assistant infrastructure on AWS.

## Prerequisites

Before beginning, ensure you have the following installed on your machine:
- AWS CLI
- Terraform
- kubectl

Ensure you are authenticated to your AWS account:
```bash
aws configure
```

## Step 1: Provision Infrastructure with Terraform

Initialize and apply the Terraform configuration:
```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

During `terraform apply`, you will be prompted to enter a password for the database. Specify a secure password.

Once completed, Terraform will print outputs including:
- `eks_cluster_name`
- `rds_endpoint`
- `redis_primary_endpoint`
- `ecr_api_url`
- `ecr_worker_url`
- `ecr_ui_url`

## Step 2: Authenticate to ECR and Push Images

Retrieve the login password and authenticate your Docker daemon to your ECR registry:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

Build the Docker images from the project root:
```bash
docker build -t arogya-api -f infra/docker/api.Dockerfile .
docker build -t arogya-worker -f infra/docker/worker.Dockerfile .
docker build -t arogya-ui -f infra/docker/ui.Dockerfile .
```

Tag the images using the repository URLs from the Terraform outputs:
```bash
docker tag arogya-api:latest <ecr_api_url>:latest
docker tag arogya-worker:latest <ecr_worker_url>:latest
docker tag arogya-ui:latest <ecr_ui_url>:latest
```

Push the images to ECR:
```bash
docker push <ecr_api_url>:latest
docker push <ecr_worker_url>:latest
docker push <ecr_ui_url>:latest
```

## Step 3: Configure Kubernetes Access

Connect `kubectl` to the newly created EKS cluster:
```bash
aws eks update-kubeconfig --region us-east-1 --name arogya-cluster
```

Verify connection:
```bash
kubectl get nodes
```

## Step 4: Configure Environment Variables

Update the image references and database connections in the deployment files located in `infra/k8s/` before deploying.

In `infra/k8s/api-deployment.yaml` and `infra/k8s/worker-deployment.yaml`, update the environment variables:
- `REDIS_URL`: Set to `redis://<redis_primary_endpoint>:6379/0`
- `DATABASE_URL`: Set to `postgresql://<db_username>:<db_password>@<rds_endpoint>/arogya`
- Update the `image` fields to use the corresponding ECR repository URLs (`<ecr_api_url>:latest`, `<ecr_worker_url>:latest`).

In `infra/k8s/ui-deployment.yaml`:
- Update the `image` field to use the ECR UI repository URL (`<ecr_ui_url>:latest`).

## Step 5: Deploy Application Components

Deploy the services and deployments:
```bash
kubectl apply -f infra/k8s/
```

Verify status of the pods:
```bash
kubectl get pods
```

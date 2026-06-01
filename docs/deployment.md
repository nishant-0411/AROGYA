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

## Step 2: Configure Kubernetes Access

Connect `kubectl` to the newly created EKS cluster:
```bash
aws eks update-kubeconfig --region us-east-1 --name arogya-cluster
```

Verify connection:
```bash
kubectl get nodes
```

## Step 3: Deploy Application components

Deploy dependencies (Redis, PostgreSQL, Qdrant) and the application deployments:
```bash
kubectl apply -f infra/k8s/
```

Verify status of the pods:
```bash
kubectl get pods
```

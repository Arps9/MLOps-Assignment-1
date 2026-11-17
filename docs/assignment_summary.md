# Assignment 1 – Orchestrating ML Workflows with Kubernetes

## Aim
Deploy a trained ML model as a scalable and resilient service using Kubernetes.

## Architecture
Iris dataset/model → FastAPI application → Docker image → Docker Hub → Kind Kubernetes cluster on AWS EC2 → Deployment and Pods → Kubernetes Service → User.

## Implemented components
- `app.py`: FastAPI web application with `/health` and `/predict`.
- `model.pkl`: reproducible Random Forest classifier trained on scikit-learn's Iris dataset.
- `Dockerfile`: packages the API, model and dependencies.
- `k8s/deployment.yaml`: Kubernetes Deployment with health probes and resource requests/limits.
- `k8s/service.yaml`: NodePort Service on port 30080.

## Kubernetes demonstration commands
```bash
kind get clusters
kubectl get nodes
kubectl create namespace mlops
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments -n mlops
kubectl get pods -n mlops
kubectl get svc -n mlops
kubectl scale deployment mlops-iris --replicas=3 -n mlops
kubectl get pods -n mlops -o wide
kubectl delete pod -n mlops POD_NAME
kubectl get pods -n mlops -w
```

## Important dataset/model note
The assignment PDF says the model was trained in Kaggle and saved as `model.pkl`, but the uploaded PDF did not include that original Kaggle notebook, dataset, or model artifact. This repository therefore includes a reproducible Random Forest model trained using scikit-learn's built-in Iris dataset. Replace `model.pkl` and adjust the input feature handling if you need to submit your exact Kaggle-trained model.

## Evidence
Capture your own screenshots of Docker build/run, Docker Hub push, Kind cluster, Pods, Service, scaling and self-healing. Do not present sample screenshots as if they came from your own environment.

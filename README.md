# MLOps Assignment 1 – Orchestrating ML Workflows with Kubernetes

**Name:** Shreyash Rajendra Pawar  
**Branch:** B.Tech CSE-DS  
**Roll No.:** 31

## Objective
Deploy a trained Iris classification model as a FastAPI service, package it with Docker, publish the image to Docker Hub, and deploy it to a Kind Kubernetes cluster. Demonstrate replicas, horizontal scaling and Kubernetes self-healing.

## Project structure
```text
MLOps-Assignment-1/
├── app.py
├── model.pkl
├── train_model.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── docs/
│   └── assignment_summary.md
└── screenshots/
```

## 1. Run locally (Windows CMD)
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
The final command above is not the server command; start the API with:
```bat
uvicorn app:app --reload
```
Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

Health check: `GET /health`  
Prediction: `POST /predict`

Example JSON:
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

## 2. Build and test Docker image
```bash
docker build -t mlops_1:1.0 .
docker images
docker run -d --name mlops_1_container -p 8000:8000 mlops_1:1.0
docker ps
docker logs mlops_1_container
```
Test `http://localhost:8000/health`, then stop/remove the test container:
```bash
docker rm -f mlops_1_container
```

## 3. Push to Docker Hub
```bash
docker login
docker tag mlops_1:1.0 YOUR_DOCKERHUB_USERNAME/mlops-iris:1.0
docker push YOUR_DOCKERHUB_USERNAME/mlops-iris:1.0
```
Replace the placeholder with your Docker Hub username.

## 4. Create Kind cluster and deploy
```bash
kind create cluster --name mlops-cluster
kind get clusters
kubectl get nodes
kubectl create namespace mlops
```
Before applying the deployment, edit `k8s/deployment.yaml` and replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username.

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments -n mlops
kubectl get pods -n mlops
kubectl get svc -n mlops
kubectl get endpoints -n mlops mlops-iris-service
```

## 5. Test service
```bash
kubectl port-forward -n mlops service/mlops-iris-service 8000:8000
```
In another terminal, test `http://localhost:8000/health` or send a POST request to `/predict`. You can also open `http://localhost:8000/docs`.

## 6. Horizontal scaling
```bash
kubectl scale deployment mlops-iris --replicas=3 -n mlops
kubectl get deployment -n mlops
kubectl get pods -n mlops -o wide
kubectl scale deployment mlops-iris --replicas=5 -n mlops
kubectl scale deployment mlops-iris --replicas=2 -n mlops
```

## 7. Self-healing demonstration
List Pods, delete one Pod, and watch Kubernetes create a replacement:
```bash
kubectl get pods -n mlops
kubectl delete pod -n mlops POD_NAME
kubectl get pods -n mlops -w
```
Replace `POD_NAME` with an actual Pod name from the first command.

## Screenshots for submission
Save genuine screenshots in `screenshots/` showing:
- Local FastAPI app and `/health` or `/predict`.
- Docker image build and running container.
- Docker Hub image.
- Kind cluster and nodes.
- Kubernetes Deployment, Pods and Service.
- Three replicas running.
- Deleted Pod and its replacement (self-healing).

## Model artifact note
The assignment PDF refers to a Kaggle-trained `model.pkl`, but the uploaded PDF did not contain that original model or Kaggle source. The included `model.pkl` is a reproducible Random Forest trained on scikit-learn's built-in Iris dataset. Use your original Kaggle model instead if exact replication of your practical is required.

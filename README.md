# URL Shortener with Splunk and Kubernetes

A self-hosted, containerized URL shortener built with **Python (Flask)**, integrated with **Splunk for observability**, containerized using **Docker**, orchestrated via **Kubernetes**, and managed through **Helm**.

## 🔧 Features

- Shorten URLs using a simple REST API
- Redirect short URLs to original URLs
- In-memory key-value storage
- Traffic logs sent to Splunk HEC (HTTP Event Collector)
- Kubernetes deployment using YAML and Helm
- Local DNS routing via `url.local`
- Ingress routing using Traefik

---

## 📁 Folder Structure

```bash
url-shortener-with-splunk/
├── url-shortener/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── url-shortener-chart/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   └── ingress.yaml
    └── url-shortener-deploy.yaml

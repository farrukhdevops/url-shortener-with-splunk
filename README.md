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
```

## ⚙️ Prerequisites

Ensure the following are installed:

- Docker Desktop  
- Kubernetes (enabled via Docker Desktop)  
- Helm  
- Git  
- Visual Studio Code (optional)  
- Splunk Enterprise  

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/farrukhdevops/url-shortener-with-splunk.git
cd url-shortener-with-splunk
```

### 2. Add Local DNS Mapping

Edit your system hosts file:

**Path (Windows):**

```
C:\Windows\System32\drivers\etc\hosts
```

Add at the bottom:

```
127.0.0.1 url.local
```

### 3. Build Docker Image

```bash
cd url-shortener
docker build -t url-shortener .
```

### 4. Enable Kubernetes

Open Docker Desktop → Settings > Kubernetes  
Enable Kubernetes and wait for the cluster to start.

### 5. Install Traefik Ingress Controller

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik
```

### 6. Deploy with Helm

```bash
cd ..\url-shortener-chart
helm install shortener .
```

**Alternative (using raw YAML):**

```bash
kubectl apply -f url-shortener-deploy.yaml
```

## 🧪 Test the Application

### 1. Shorten a URL

```bash
curl -X POST http://url.local:30080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com"}'
```

### 2. Access the Short URL

Visit:

```
http://url.local:30080/<short_id>
```

## 📊 Splunk Integration

### 1. Enable HEC (HTTP Event Collector)

In Splunk:

- Go to Settings > Data Inputs > HTTP Event Collector  
- Click New Token  
- Name: `url-logs`  
- Copy the token after creation  
- Enable:
  - "All Tokens"
  - "Enable SSL"

### 2. Update `app.py`

Update the following:

```python
SPLUNK_HEC_URL = "http://host.docker.internal:8088/services/collector/event"
SPLUNK_TOKEN = "your-splunk-token"
```

### 3. Test Splunk Logging

```bash
curl -X POST http://host.docker.internal:8088/services/collector/event \
  -H "Authorization: Splunk <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"event": "test event", "sourcetype": "url-shortener"}'
```

### 4. View Logs in Splunk

Go to Search & Reporting and run:

```spl
index=main sourcetype="url-shortener"
```

## ⚠️ Notes

This project is for demonstration purposes.

- URL mappings are stored in-memory, so they are lost on restart.

For production:

- Add persistent DB (PostgreSQL, Redis)
- Add HTTPS support
- Use authentication & rate-limiting

## 🧑‍💻 Author

**Farrukh Ejaz**  
[GitHub Profile](https://github.com/farrukhdevops)

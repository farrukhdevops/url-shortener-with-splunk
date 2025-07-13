URL Shortener with Splunk and Kubernetes
This project is a fully containerized, self-hosted URL shortener written in Python using Flask. It includes observability via Splunk HEC (HTTP Event Collector), containerization with Docker, orchestration with Kubernetes, and reverse proxy routing using Traefik.

Features
Shorten URLs via a REST API

Redirect short URLs to original URLs

In-memory storage

Traffic logs sent to Splunk for analysis

Kubernetes deployment using Helm and YAML

Local DNS mapping via url.local

Prerequisites
You must have the following installed on your system:

Docker Desktop

Kubernetes (via Docker Desktop)

Helm

VS Code (optional)

Git

Splunk Enterprise

Folder Structure
pgsql
Copy
Edit
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
How to Run Locally
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/farrukhdevops/url-shortener-with-splunk.git
cd url-shortener-with-splunk
2. Add Local DNS
Edit your hosts file:

Path:

makefile
Copy
Edit
C:\Windows\System32\drivers\etc\hosts
Add this line at the bottom:

lua
Copy
Edit
127.0.0.1 url.local
3. Build Docker Image
bash
Copy
Edit
cd url-shortener
docker build -t url-shortener .
4. Enable Kubernetes in Docker Desktop
Open Docker Desktop

Go to Settings > Kubernetes

Enable Kubernetes and wait for it to start

5. Install Traefik Ingress Controller
bash
Copy
Edit
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik
6. Deploy App with Helm
bash
Copy
Edit
cd ..\url-shortener-chart
helm install shortener .
Or deploy with raw YAML (alternative):

bash
Copy
Edit
kubectl apply -f url-shortener-deploy.yaml
Test the Application
Shorten URL
bash
Copy
Edit
curl -X POST http://url.local:30080/shorten `
     -H "Content-Type: application/json" `
     -d '{"url": "https://youtube.com"}'
Redirect URL
Visit: http://url.local:30080/<short_id> in your browser.

Splunk Integration
1. Enable HTTP Event Collector in Splunk
Settings > Data Inputs > HTTP Event Collector > New Token

Name: url-logs

Token: Copy it

Enable All Tokens and Enable SSL options

2. Update app.py
Edit the following in app.py:

python
Copy
Edit
SPLUNK_HEC_URL = "http://host.docker.internal:8088/services/collector/event"
SPLUNK_TOKEN = "<your-token-here>"
3. Validate Splunk Logging
Send test:

bash
Copy
Edit
curl -X POST http://host.docker.internal:8088/services/collector/event `
     -H "Authorization: Splunk <your-token>" `
     -H "Content-Type: application/json" `
     -d '{"event": "test event", "sourcetype": "url-shortener"}'
Search logs in Splunk under Search & Reporting using:

spl
Copy
Edit
index=main sourcetype="url-shortener"
Notes
This is a development/demo project.

Data is stored in memory (resets on restart).

Production use would require:

Persistent DB

HTTPS and TLS certs

Authentication and rate limiting

Author
Farrukh Ejaz

# Cybersecurity Content Moderator

## Overview
This project is a **Cybersecurity Content Moderator** that uses an **Ollama LLM model** (`cyber-moderator-Wlm:7b`) to detect and classify harmful content. It integrates **FastAPI** for the backend and **Streamlit** for the frontend, with **FAISS** for efficient similarity search.

---

## Features
- ✅ **Text & PDF Moderation**: Supports both plain text and PDF files.
- 🤖 **AI-Powered Content Analysis**: Uses a custom-trained Ollama model.
- 🔍 **Semantic Search**: Retrieves similar content using **FAISS** and **Sentence Transformers**.
- 🖥 **User-Friendly UI**: Built with Streamlit.

---

## API Endpoints
| Endpoint         | Method | Description |
|-----------------|--------|-------------|
| `/upload-text/` | POST   | Accepts text for moderation |
| `/upload-pdf/`  | POST   | Accepts a PDF file for analysis |
| `/retrieve-chunks/` | GET | Retrieves similar content |

---

## Installation (Without Containerization)

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Ollama installed and running
- GPU support for model inference (recommended)

### Clone the Repository
```bash
git clone https://github.com/harish-nika/cybersecurity_moderator.git
cd cybersecurity_moderator/codes
```

### Create a Virtual Environment
```bash
python -m venv gpuenv
source gpuenv/bin/activate  # On Linux/macOS
gpuenv\Scripts\activate  # On Windows
```

### Install Dependencies
```bash
pip install --no-cache-dir -r requirements.txt
```

---

## Model Setup (Ollama)

### 1️⃣ Create and Configure the Ollama Model File
Navigate to the `modelfiles` directory and create an Ollama `Modelfile`:

```bash
cd /home/harish/workspace_dc/cybersecurity_moderator/modelfiles/
nano Modelfile
```

Inside the `Modelfile`, define your model configuration:

```dockerfile
# Ollama Model Configuration File
FROM wizardlm2:7b
SYSTEM "Cybersecurity content moderation model"
PARAMETER "temperature" 0.7
PARAMETER "top_p" 0.9
```

Save and exit (`Ctrl + X`, then `Y`, and `Enter`).

### 2️⃣ Build the Ollama Model
```bash
ollama create cyber-moderator-Wlm:7b -f /home/harish/workspace_dc/cybersecurity_moderator/modelfiles/Modelfile
```

### 3️⃣ Verify the Model
```bash
ollama list
```

### 4️⃣ Start Using the Model
```bash
OLLAMA_USE_CUDA=1 ollama run cyber-moderator-Wlm:7b "Analyze this message for harmful content."
```

---

## Running the Application (Without Containerization)

### Start the Backend (FastAPI)
```bash
chmod +x /app/backend/start.sh
bash /app/backend/start.sh
```

### Start the Frontend (Streamlit)
```bash
chmod +x /app/frontend/start_frontend.sh
bash /app/frontend/start_frontend.sh
```

---

# Content Moderator - Containerization Guide

## Project Structure
```
Content-moderator-image/
│-- backend/
│   ├── backend.py  # FastAPI backend
│   ├── start.sh  # Backend start script
│   └── requirements.txt  # Dependencies
│
│-- frontend/
│   ├── frontend.py  # Streamlit frontend
│   ├── start_frontend.sh  # Frontend start script
│   └── requirements.txt  # Dependencies
│
│-- models/
│   └── Modelfile  # Ollama model configuration
│
│-- docker/
│   └── Dockerfile  # Docker build instructions
│
│-- start_service.sh  # Master startup script
│-- docker-compose.yml  # Docker Compose configuration
```

---

## Containerization Process
### **1. Dockerfile**
```dockerfile
# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose necessary ports
EXPOSE 8000 8501

# Make scripts executable
RUN chmod +x start_service.sh backend/start.sh frontend/start_frontend.sh

# Use ENTRYPOINT instead of CMD for better control
ENTRYPOINT ["/bin/bash", "start_service.sh"]
```

### **2. Docker Compose Configuration (`docker-compose.yml`)**
```yaml
version: "3.8"

services:
  ollama:
    image: ollama/ollama
    container_name: ollama_server
    restart: always
    ports:
      - "11434:11434"
    volumes:
      - ./models:/root/.ollama/models  # Persist model files
    healthcheck:
      test: ["CMD", "ollama", "list"]
      interval: 10s
      retries: 3

  backend:
    build: .
    container_name: content_moderator_backend
    depends_on:
      ollama:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    command: ["/bin/bash", "/app/backend/start.sh"]

  frontend:
    build: .
    container_name: content_moderator_frontend
    depends_on:
      - backend
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    command: ["/bin/bash", "/app/frontend/start_frontend.sh"]
```

### **3. Build and Run the Docker Container**
```bash
docker-compose up --build
```
To stop:
```bash
docker-compose down
```
### **3. frontend  Configuration (`start_services.sh`)**
```sh
#!/bin/bash

echo "🔄 Starting Ollama server..."
ollama serve &

# Wait for Ollama to start
sleep 10  # Ensure Ollama is running before pulling models

echo "📥 Pulling base model..."
ollama pull wizardlm2:7b

echo "🛠 Creating custom moderation model..."
ollama create cyber-moderator-Wlm:7b -f /app/models/Modelfile  # Absolute path

echo "🚀 Starting Backend..."
bash /app/backend/start.sh &

echo "🎨 Starting Frontend..."
bash /app/frontend/start_frontend.sh


```

### **4. frontend  Configuration (`start_frontend.sh`)**
```sh
#!/bin/bash

echo "🎨 Starting Streamlit Frontend..."
cd /app/frontend  # Ensure correct directory
streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0

```

### **5. backend  Configuration (`start.sh`)**
```sh
#!/bin/bash

echo "🚀 Starting FastAPI Backend..."
cd /app/backend  # Ensure correct directory

# Ensure correct module path
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

```

### **6. Build and Run the Docker Container**
```bash
docker-compose up --build
```
To stop:
```bash
docker-compose down
```

### **7. workflow  Configuration (`docker-build.yml`)**
```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
    tags:
      - 'v*'  # Trigger build only when a version tag like v1.0.1 is pushed to main
  workflow_dispatch:  # Allow manual trigger

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Get Latest Tag and Generate New Version
      id: versioning
      run: |
        git fetch --tags
        LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
        if [ -z "$LATEST_TAG" ]; then
          NEW_TAG="v1.0.0"
        else
          NEW_TAG=$(echo "$LATEST_TAG" | awk -F. -v OFS=. '{ $NF += 1 ; print }')
        fi
        echo "NEW_TAG=$NEW_TAG" >> $GITHUB_ENV
        echo "New version: $NEW_TAG"

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build Docker Image (Using Correct Dockerfile Path)
      run: |
        docker build -t harishkumarthesde/content-moderator:latest -f docker/Dockerfile .
        docker tag harishkumarthesde/content-moderator:latest harishkumarthesde/content-moderator:${{ env.NEW_TAG }}

    - name: Push Docker Image
      run: |
        docker push harishkumarthesde/content-moderator:latest
        docker push harishkumarthesde/content-moderator:${{ env.NEW_TAG }}

    - name: Push New Git Tag (Only if Pushed to Main)
      if: github.ref == 'refs/heads/main'
      run: |
        git config --global user.email "harishkumar56278@gmail.com"
        git config --global user.name "harish-nika"
        git fetch --tags
        git tag ${{ env.NEW_TAG }}
        git push origin ${{ env.NEW_TAG }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Use GitHub’s built-in token


```


---

## **Output Screenshots**
### Backend Processing Output
![Backend Running](Content-moderator-image/images/code.png)

### Streamlit Moderation Interface Output
![Streamlit UI Output](images/site-streamlit-out.png)
![Streamlit UI Output](images/site-streamlit.png)

### GitHub Actions Build & Run Output
![GitHub Actions Build & Run](images/builda.png)
![GitHub Actions Build & Run](images/buildb.png)

---

## **License**
This project is licensed under the **MIT License**.

## **Author**
- **Harish Kumar S**
- GitHub: [Harish-nika](https://github.com/Harish-nika)
- Email: [harishkumar56278@gmail.com](mailto:harishkumar56278@gmail.com)
- Portfolio: [Harish Kumar S - AI ML Engineer](https://harish-nika.github.io/)


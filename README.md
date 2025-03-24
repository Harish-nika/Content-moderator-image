# Cybersecurity Content Moderator

## Overview
This project is a **Cybersecurity Content Moderator** that uses an **Ollama LLM model** (`cyber-moderator-G3:27b`) to detect and classify harmful content. It integrates **FastAPI** for the backend and **Streamlit** for the frontend, with **FAISS** for efficient similarity search.

---

## Features
- **Text & PDF Moderation**: Supports both plain text and PDF files.
- **AI-Powered Content Analysis**: Uses a custom-trained Ollama model.
- **Semantic Search**: Retrieves similar content using **FAISS** and **Sentence Transformers**.
- **User-Friendly UI**: Built with Streamlit.

---

## Installation (Without Containerization)

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Ollama installed and running
- GPU support for model inference (recommended)

### Clone the Repository
```bash
git clone https://github.com/your-repo/cybersecurity_moderator.git
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
pip install -r requirements.txt
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

```plaintext
# Ollama Model Configuration File
FROM llama3.3:70b
SYSTEM "Cybersecurity content moderation model"
PARAMETER "temperature" 0.7
PARAMETER "top_p" 0.9
```

Save and exit (`Ctrl + X`, then `Y`, and `Enter`).

### 2️⃣ Build the Ollama Model
```bash
ollama create cyber-moderator-G3:27b -f /home/harish/workspace_dc/cybersecurity_moderator/modelfiles/Modelfile
```

### 3️⃣ Verify the Model
```bash
ollama list
```

### 4️⃣ Start Using the Model
```bash
ollama run cyber-moderator-G3:27b "Analyze this message for harmful content."
```

---

## Running the Application (Without Containerization)

### Start the Backend (FastAPI)
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

### Start the Frontend (Streamlit)
```bash
streamlit run frontend.py
```

---

# Content Moderator - Containerization Guide

## Project Structure
```
Content-moderator-image/
│-- backend/
│   ├── main.py  # FastAPI backend
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
│-- start_services.sh  # Master startup script
│-- docker-compose.yml  # Docker Compose configuration
```

---

## Containerization Process
### **1. Dockerfile**
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt
RUN curl -fsSL https://ollama.com/install.sh | sh
EXPOSE 8000 8501
CMD ["/bin/bash", "start_services.sh"]
```

### **2. Docker Compose Configuration (`docker-compose.yml`)**
```yaml
version: "1.1"
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - ollama

  frontend:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - backend

  ollama:
    image: ollama/ollama
    restart: always
    ports:
      - "11434:11434"
```

### **3. Build and Run the Docker Container**
```bash
docker build -t harishkumarthesde/content-moderator:latest .
docker run -p 8000:8000 -p 8501:8501 harishkumarthesde/content-moderator:latest
```

### **4. Using Docker Compose**
```bash
docker-compose up --build
```
To stop:
```bash
docker-compose down
```

---

## **Output Screenshots**

### Backend Processing Output
![Backend Running](Content-moderator-image/images/code.png)

### Streamlit Moderation Interface Output
![Streamlit UI Output](Content-moderator-image/images/site-streamlit-out.png)
![Streamlit UI Output](Content-moderator-image/images/site-streamlit.png)

### GitHub Actions Build & Run Output
![GitHub Actions Build & Run](Content-moderator-image/images/builda.png)
![GitHub Actions Build & Run](Content-moderator-image/images/buildb.png)
---

## **Conclusion**
You have successfully set up and deployed the **Cybersecurity Content Moderator**, both with and without containerization. You can now pull and run it from **Docker Hub** or run it manually.

Happy coding! 🚀

## **License**
This project is licensed under the **MIT License**.

## **Author**
- **Harish Kumar S**
- GitHub: [Harish-nika](https://github.com/Harish-nika)
- Email: [harishkumar56278@gmail.com](mailto:harishkumar56278@gmail.com)
- Portfolio: [Harish Kumar S - AI ML Engineer](https://harish-nika.github.io/)


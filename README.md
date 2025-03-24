# Content Moderator - Containerization Guide

## Overview
This guide explains how the **Content Moderator** application is containerized using Docker and how to pull and execute it from Docker Hub.

---

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
# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose necessary ports
EXPOSE 8000 8501

# Run startup script
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

### **3. Startup Script (`start_services.sh`)**
```bash
#!/bin/bash

echo "🔄 Starting Ollama server..."
ollama serve &

# Wait for Ollama to start
sleep 10

echo "📥 Pulling base model..."
ollama pull wizardlm2:7b

echo "🫠 Creating custom moderation model..."
ollama create cyber-moderator-Wlm:7b -f /app/models/Modelfile

echo "🚀 Starting Backend..."
bash /app/backend/start.sh &

echo "🎨 Starting Frontend..."
bash /app/frontend/start_frontend.sh
```

---

## **Building and Running the Docker Container**

### **1. Build the Docker Image**
Run the following command inside the project directory:
```sh
docker build -t harishkumarthesde/content-moderator:latest .
```

### **2. Verify Image is Built**
```sh
docker images
```
You should see `harishkumarthesde/content-moderator` in the list.

### **3. Run the Container**
```sh
docker run -p 8000:8000 -p 8501:8501 harishkumarthesde/content-moderator:latest
```

---

## **Pushing the Image to Docker Hub**
### **1. Log in to Docker Hub**
```sh
docker login
```

### **2. Tag the Image**
```sh
docker tag harishkumarthesde/content-moderator:latest harishkumarthesde/content-moderator:latest
```

### **3. Push the Image**
```sh
docker push harishkumarthesde/content-moderator:latest
```

---

## **Pull and Run from Docker Hub**
### **1. Pull the Image**
```sh
docker pull harishkumarthesde/content-moderator:latest
```

### **2. Run the Container**
```sh
docker run -p 8000:8000 -p 8501:8501 harishkumarthesde/content-moderator:latest
```

Now, the **FastAPI backend** will be accessible at `http://localhost:8000` and the **Streamlit frontend** at `http://localhost:8501`.

---

## **Running with Docker Compose**
Instead of running containers manually, use **Docker Compose** for easier orchestration:
```sh
docker-compose up --build
```
This will start all services (backend, frontend, and Ollama) automatically.

To stop, use:
```sh
docker-compose down
```

---

## **Conclusion**
You have successfully containerized and deployed the **Content Moderator** application. You can now pull and run it from **Docker Hub** with ease.

Happy coding! 🚀

## License

This project is licensed under the **MIT License**.

## Author

- **Harish Kumar S**
- GitHub: [Harish-nika](https://github.com/Harish-nika)
- Email: [harishkumar56278@gmail.com](mailto\:harishkumar56278@gmail.com)
- portfolio: [Harish Kumar S - AI ML Engineer](https://harish-nika.github.io/)


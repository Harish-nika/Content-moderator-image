# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements files from the docker directory
COPY docker/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Now copy the entire application AFTER installing dependencies
COPY . /app

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose necessary ports
EXPOSE 8000 8501

# Make scripts executable
RUN chmod +x start_services.sh backend/start.sh frontend/start_frontend.sh

# Use ENTRYPOINT for better control over container startup
ENTRYPOINT ["/bin/bash", "/app/start_services.sh"]

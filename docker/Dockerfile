# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements files first to leverage Docker layer caching
COPY backend/requirements.txt frontend/requirements.txt ./

# Ensure the file is correctly copied
RUN ls -l backend/requirements.txt || echo "backend/requirements.txt not found!"
RUN ls -l frontend/requirements.txt || echo "frontend/requirements.txt not found!"

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Now copy the entire application AFTER installing dependencies
COPY . .

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose necessary ports
EXPOSE 8000 8501

# Make scripts executable
RUN chmod +x start_services.sh backend/start.sh frontend/start_frontend.sh

# Use ENTRYPOINT instead of CMD for better control
ENTRYPOINT ["/bin/bash", "start_services.sh"]

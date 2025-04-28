FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Install additional dependencies
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /workspace

# Copy requirements.txt and install Python dependencies
COPY Web-Chatbot/requirements.txt /workspace/
RUN pip install -r requirements.txt

# Verify installation
RUN pip list
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies, including Graphviz
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apertium-all-dev \
    graphviz && \
    rm -rf /var/lib/apt/lists/*  # This cleans up cached package lists to reduce image size

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to ensure Python output is sent directly to terminal
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]
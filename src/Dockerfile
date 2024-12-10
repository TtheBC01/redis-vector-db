# Use the official Python 3.10 image as the base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first (for dependency caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
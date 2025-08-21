# Use official Python image

# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for X11 GUI support
RUN apt-get update && apt-get install -y \
	libx11-6 \
	libxext6 \
	libxrender1 \
	libsm6 \
	libxrandr2 \
	libxcb1 \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app

# Set environment variable for X11 forwarding
ENV DISPLAY=:0

# Default command: run the GUI app
CMD ["python3", "app/main.py"]

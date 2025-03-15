# Use an official Python runtime as a parent image.
# Note: changed from 3.11 to 3.9 due to docker build issue when installing Foil (sub directory) for 1 or more packages
FROM python:3.9

# Set the working directory in the container
WORKDIR /cryptoapp

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/cryptoapp

# Copy requirements.txt and install dependencies
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend directory into the container at /cryptoapp/backend
COPY backend /cryptoapp/backend

# Copy frontend directory into the container at /cryptoapp/frontend
COPY frontend /cryptoapp/frontend

# Copy database directory into the container at /cryptoapp/database
COPY database /cryptoapp/database

# Copy docker directory into the container at /cryptoapp/docker
COPY docker /cryptoapp/docker

# Run the Python script
CMD ["python", "backend/main.py"]
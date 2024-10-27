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

# Copy app directory into the container at /cryptoapp/app
COPY app /cryptoapp/app

# Copy docker directory into the container at /cryptoapp/docker
COPY docker /cryptoapp/docker

# Run the Python script
CMD ["python", "app/process_flows/table_composer.py", "trial_email_flow"]
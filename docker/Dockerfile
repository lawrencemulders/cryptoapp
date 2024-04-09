# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the cryptoapp directory into the container at /app/cryptoapp
COPY .. /app/cryptoapp

# Set the working directory to the cryptoapp directory
WORKDIR /app/cryptoapp

# Install needed dependencies
RUN pip install --no-cache-dir -r docker/requirements.txt

# Run the Python script
CMD ["python", "email_flow.py", "schedule_email_flow"]
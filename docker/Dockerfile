# Use an official Python runtime as a parent image
FROM python:3.11

# Copy the contents of the cryptoapp directory into the container at /app/cryptoapp
COPY .. /app/cryptoapp

# Set the working directory to the cryptoapp directory
WORKDIR /app/cryptoapp

# Define build argument for the path to requirements.txt
ARG REQUIREMENTS_FILE=requirements.txt

# Install needed dependencies
RUN pip install --no-cache-dir -r $REQUIREMENTS_FILE

# Run the Python script
CMD ["python", "email_flow.py", "schedule_email_flow"]
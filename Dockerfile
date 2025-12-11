# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Define environment variables if necessary (optional)
# ENV CORONA_PAT your_pat
# ENV CORONA_HOST your_corona_host
# ENV MAX_REQ_TIMEOUT=120

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
# Copy the SPDX file into the container at /app - TEMP FOR TESTING
COPY bes-traceability-spdx.json /app/
# Copy the application package into the container
COPY src/upload_spdx /app/upload_spdx

# Upgrade pip & Install dependency packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the Python package when the container launches
ENTRYPOINT ["python3", "-m", "upload_spdx"]

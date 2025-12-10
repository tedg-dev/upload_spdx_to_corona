# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Define environment variables if necessary (optional)
# ENV CORONA_PAT your_pat
# ENV CORONA_HOST your_corona_host
# ENV MAX_REQ_TIMEOUT=120

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
# Copy the SPDX file into the container at /app - TEMP FOR TESTING
COPY bes-traceability-spdx.json /app/
# Copy the application code into the container
COPY src/upload_spdx.py /app/upload_spdx.py

# Upgrade pip & Install dependency packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the Python script when the container launches
ENTRYPOINT ["python3"]
CMD ["upload_spdx.py"]
#ENTRYPOINT ["python3", "upload_spdx.py"]

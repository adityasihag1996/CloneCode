# Use the official Python image as a parent image
FROM python:3.10-slim
# FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the Python script from your host to the container's working directory
# COPY runner.py /app/
# COPY tasks.py /app/

# RUN apt-get update && apt-get install redis-server -y

# Install any needed packages specified in requirements.txt
# Here we are installing redis and rq directly, but you could use a requirements.txt file as well
# RUN pip install --no-cache-dir redis rq

# Run the script when the container launches
# CMD ["python", "runner.py"]

# Keep the container running
CMD ["tail", "-f", "/dev/null"]
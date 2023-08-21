# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Install build essentials and gcc
RUN apt-get update && apt-get install -y build-essential portaudio19-dev

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
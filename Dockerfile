# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Update Ubuntu and install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory in the container
WORKDIR /katip

# Copy the current directory contents into the container at /app
COPY . /katip

# Update Ubuntu and install Python
RUN pip3 install -r requirements.txt

# Run app.py when the container launches
CMD ["sh", "-c", "start.sh"]
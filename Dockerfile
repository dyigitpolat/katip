# Use an official Ubuntu as a parent image
FROM python:3.12-bullseye

# Set the working directory in the container
WORKDIR /katip

# Copy the current directory contents into the container at /app
COPY . /katip

# Update Ubuntu and install Python
RUN pip3 install -r requirements.txt
RUN chmod 777 start.sh

# Run app.py when the container launches
CMD ./start.sh
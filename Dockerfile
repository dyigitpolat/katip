# Use an official Ubuntu as a parent image
FROM python:3.12-bullseye

# Set the working directory in the container
WORKDIR /katip

# Copy the current directory contents into the container at /app
COPY . /katip

# Update Ubuntu and install Python
RUN python3 -m venv env
RUN source env/bin/activate
RUN pip3 install -r requirements.txt

# Run app.py when the container launches
CMD ["sh", "-c", "start.sh"]
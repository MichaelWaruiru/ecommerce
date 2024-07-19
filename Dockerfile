# Set official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any packages specified in requirements.txt
RUN pip Install --no-cache-directory -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 80 available outside this container
EXPOSE 80

# Run app.py
CMD [ "python", "app.py" ]
# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /todo

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY /todo .

# Expose the desired port for the Django app to run on
EXPOSE 8000

# Start the Django app using gunicorn
CMD ["gunicorn", "todo.wsgi:application", "--bind", "0.0.0.0:8000"]
# Dockerfile.django

# Use Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copy the requirements file to install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY ./llm /usr/src/app/

# Expose the port for the Django server
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

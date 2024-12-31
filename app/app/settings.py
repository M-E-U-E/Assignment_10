import os

# Allowed hosts should include the necessary domains, container name, or IPs
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,django_app').split(',')

# Database configuration with environment variables and sensible defaults
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'hotel_db'),
        'USER': os.getenv('POSTGRES_USER', 'username'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),  # Ensure 'db' matches the service name in docker-compose.yml
        'PORT': int(os.getenv('POSTGRES_PORT', 5432)),  # Convert to int for Django compatibility
    }
}

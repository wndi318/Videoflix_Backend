
# Videoflix Backend

This is the backend for the Videoflix application, built with Django and Django REST Framework. It provides API endpoints for video management, user authentication, and more. The backend uses Redis for caching and task queues, with Nginx and Gunicorn for deployment.

## Prerequisites

Ensure you have the following dependencies installed before starting:

- Python 3.8 or higher
- Django 4.2.16
- Redis
- Nginx
- Gunicorn
- Supervisor (optional for process management)

## Installation

### 1. Clone the Repository

Clone the project to your local machine:

```bash
git clone <REPO_URL>
cd Videoflix_Backend
```

### 2. Set Up Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

Install all the required Python dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Install Redis

Redis is required for caching and task queue management. Install Redis on your server:

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory and configure your environment variables:

```bash
SECRET_KEY=<your-secret-key>
RQ_PASSWORD=<your-redis-password>
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-email-password>
```

### 6. Apply Database Migrations

Run the migrations to set up the database:

```bash
python manage.py migrate
```

### 7. Create a Superuser

Create an admin user for accessing the Django admin interface:

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

Collect all static files so that they can be served by Nginx:

```bash
python manage.py collectstatic
```

### 9. Gunicorn and Nginx Configuration

#### Gunicorn Setup

Start Gunicorn with the following command:

```bash
gunicorn --workers 3 videoflix.wsgi:application
```

#### Nginx Setup

Create a new Nginx configuration file (e.g., `/etc/nginx/sites-available/videoflix`) and add the following configuration:

```nginx
server {
    listen 80;
    server_name <your-server-ip>;

    location /static/ {
        root /home/<user>/projects/Videoflix_Backend/videoflix/staticfiles;
    }

    location / {
        proxy_pass http://unix:/home/<user>/projects/Videoflix_Backend/videoflix/videoflix.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Link the configuration to the Nginx `sites-enabled` directory and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/videoflix /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

### 10. Supervisor Setup (Optional)

Use Supervisor to manage Gunicorn processes automatically. Create a Supervisor configuration file at `/etc/supervisor/conf.d/videoflix_gunicorn.conf`:

```ini
[program:videoflix_gunicorn]
command=/home/<user>/projects/Videoflix_Backend/env/bin/gunicorn --workers 3 --bind unix:/home/<user>/projects/Videoflix_Backend/videoflix/videoflix.sock videoflix.wsgi:application
directory=/home/<user>/projects/Videoflix_Backend/videoflix
autostart=true
autorestart=true
stderr_logfile=/var/log/videoflix/gunicorn.err.log
stdout_logfile=/var/log/videoflix/gunicorn.out.log
```

Reload Supervisor and start the Gunicorn service:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start videoflix_gunicorn
```

## API Endpoints

- `/videos/`: Get a list of all videos
- `/videos/<id>/`: Get details of a specific video
- `/register/`: User registration
- `/login/`: User login
- `/logout/`: User logout

## Running Tests

To run tests and check coverage:

```bash
coverage run manage.py test
coverage report
```

## Deployment

After setting up Gunicorn and Nginx, the backend should be fully accessible via your server IP or domain. The Angular frontend should communicate with this backend via the configured API endpoints.

## Running the Project

If you close your SSH session, use Supervisor to ensure the application keeps running:

```bash
sudo supervisorctl start videoflix_gunicorn
```

## License

This project is licensed under the MIT License.

---

### Notes:

1. Replace the placeholder values like `<user>`, `<your-server-ip>`, and `<your-secret-key>` with the actual values.
2. This `README.md` contains all necessary steps for setting up and running the backend, so anyone cloning the project can follow along easily.
3. You may want to adjust paths, IPs, and other settings depending on your deployment environment.

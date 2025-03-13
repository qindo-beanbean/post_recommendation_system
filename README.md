## Features

1. User authentication (signup, login, logout)
2. Create posts with text content
3. Like/unlike posts
4. View a dashboard of all posts sorted by popularity

## Teck Stack
Backend: Flask, Python 3.9+
Database: SQLite
Authentication: Flask-Login

## Installation
1. Clone the repository from github
```bash
git clone https://github.com/qindo-beanbean/post-recommendation-app.git
cd post-recommendation-app
```
2. Create and activate a virtual environment/or use Docker
```bash
python -m venv venv
source venv/bin/activate 
```
or
```bash
docker run -it --rm -p 8080:5000 -v $(pwd):/app -w /app python:3.9 bash -c "pip install -r requirements.txt && FLASK_APP=app.py FLASK_DEBUG=1 flask run --host=0.0.0.0"
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Configure
```bash
mkdir -p instance
```
5. Initialize database
```bash
flask run
```

Then access the application at http://localhost:5000, if use Docker, at http://localhost:8080

## Deployment

The application is deployed on PythonAnywhere
# post_recommendation_system

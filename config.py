import os
from datetime import timedelta

class Config:
    # Security configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///posts.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload file configuration
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  
import os
from flask import Flask, render_template
from flask_login import LoginManager
from datetime import datetime
from models import db, User
from routes import main

def create_app(test_config=None):
    # Create app
    app = Flask(__name__, instance_relative_config=True)
    
    # Loading configuration
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
      
    from config import Config
    app.config.from_object(Config)
    
    # Error
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Upload file exist
    upload_folder = os.path.join(app.static_folder, app.config['UPLOAD_FOLDER'].split('/', 1)[1])
    os.makedirs(upload_folder, exist_ok=True)
    
    # Initialize db
    db.init_app(app)
    
    # Create DB
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in first'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(main)
    
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
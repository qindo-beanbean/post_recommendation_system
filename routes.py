import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Post
from datetime import datetime
import uuid

# Blueprint
main = Blueprint('main', __name__)

# Check filename 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return new_filename

# Home route
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

# Register route
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # validation
        if not email or not password:
            flash('Please enter email and password', 'danger')
            return redirect(url_for('main.signup'))
        
        if password != password_confirm:
            flash('Password does not match', 'danger')
            return redirect(url_for('main.signup'))
        
        # check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email has been registered', 'danger')
            return redirect(url_for('main.signup'))
        
        # Create new user
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Success, please log in', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('signup.html')

# Sign in route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Check password
        if not user or not user.check_password(password):
            flash('Wrong email or password', 'danger')
            return redirect(url_for('main.login'))
        
        # Sign in user
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        
        flash('Success', 'success')
        return redirect(next_page or url_for('main.dashboard'))
    
    return render_template('login.html')

# Sign out route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have signed out', 'info')
    return redirect(url_for('main.login'))

# Dashboard route
@main.route('/dashboard')
@login_required
def dashboard():
    # Fetch post
    posts = Post.query.all()
    # sort post
    sorted_posts = sorted(posts, key=lambda post: post.like_count, reverse=True)
    
    return render_template('dashboard.html', posts=sorted_posts)

# Create post route
@main.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content:
            flash('Please enter a value', 'danger')
            return redirect(url_for('main.create_post'))
        
        new_post = Post(content=content, user_id=current_user.id)
        
        # Image upload
        # if 'image' in request.files:
        #     file = request.files['image']
        #     if file and file.filename != '' and allowed_file(file.filename):
        #         filename = generate_unique_filename(secure_filename(file.filename))
        #         upload_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
                
        #         # check if upload exist
        #         if not os.path.exists(upload_path):
        #             os.makedirs(upload_path)
                
        #         file_path = os.path.join(upload_path, filename)
        #         file.save(file_path)
        #         new_post.image = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        db.session.add(new_post)
        db.session.commit()
        
        flash('Posted!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('post_form.html')

# Like API
@main.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if user like
    if current_user.has_liked_post(post):
        # Cancel like
        current_user.unlike_post(post)
        db.session.commit()
        return jsonify({'status': 'success', 'action': 'unliked', 'count': post.like_count})
    else:
        # Add like
        current_user.like_post(post)
        db.session.commit()
        return jsonify({'status': 'success', 'action': 'liked', 'count': post.like_count})
    

@main.route('/debug/database')
@login_required
def debug_database():
    
    # Fetch user data
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'email': user.email,
        })
    
    # Fetch post data
    posts = Post.query.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'content': post.content[:50] + "..." if len(post.content) > 50 else post.content,
            'user_id': post.user_id,
            'timestamp': post.timestamp,
            'like_count': post.like_count,
            'image': post.image,
        })
    
    # Return data
    return jsonify({
        'users': users_data,
        'posts': posts_data
    })
    

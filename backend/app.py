from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from models import Complaint
from extensions import db  # ✅ FIXED
from routes.auth_routes import auth_bp
from routes.chatbot_routes import chatbot_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register blueprints
app.register_blueprint(chatbot_bp)
app.register_blueprint(auth_bp)
# app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return render_template('login.html')

from flask import session, redirect, url_for, render_template
import os

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    user_id = session['user_id']
    return render_template('dashboard.html', user_id=user_id)

@app.route('/report', methods=['POST'])
def report():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    image = request.files['image']
    description = request.form['description']
    location = request.form['location']

    # Save uploaded image
    uploads_dir = os.path.join(app.root_path, 'static/uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    image_path = os.path.join(uploads_dir, image.filename)
    image.save(image_path)

    # TODO: Save report info to DB and run YOLO detection later
    flash('Report submitted successfully!', 'success')
    return redirect(url_for('dashboard'))


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    name = request.form['name']
    phone = request.form['phone']
    issue_type = request.form['issue_type']
    location = request.form['location']
    image = request.files['image']

    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    # TODO: Integrate YOLOv8 detection here later
    new_complaint = Complaint(
        name=name,
        phone=phone,
        issue_type=issue_type,
        location=location,
        image_path=filepath
    )

    db.session.add(new_complaint)
    db.session.commit()

    flash("Complaint submitted successfully!")
    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

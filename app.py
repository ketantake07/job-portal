from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'worktoday-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///job_portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

# Models
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # it, non-it, gov, fresher, internship, remote, experienced, hackathons, trainee
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    salary = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    company_url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    applications = db.relationship('Application', backref='job', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    resume = db.Column(db.String(500))
    cover_letter = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('home.html', jobs=jobs)

@app.route('/category/<category>')
def category_jobs(category):
    if category == 'fresher':
        # Show jobs with fresher category OR 0-1 years experience
        jobs = Job.query.filter(
            (Job.category == 'fresher') | (Job.experience == '0-1 years')
        ).order_by(Job.created_at.desc()).all()
    elif category == 'it':
        # Show IT jobs including fresher IT jobs
        jobs = Job.query.filter(
            (Job.category == 'it') | 
            ((Job.category == 'fresher') & (Job.title.contains('Developer') | Job.title.contains('Engineer') | Job.title.contains('Programmer') | Job.title.contains('Software')))
        ).order_by(Job.created_at.desc()).all()
    else:
        jobs = Job.query.filter_by(category=category).order_by(Job.created_at.desc()).all()
    
    return render_template('category.html', jobs=jobs, category=category)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    resume_url = ''
    # Handle resume file upload
    if 'resume_file' in request.files:
        file = request.files['resume_file']
        if file and file.filename != '':
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resume_url = url_for('static', filename='uploads/' + filename)
    
    application = Application(
        job_id=job_id,
        name=request.form['name'],
        email=request.form['email'],
        phone=request.form['phone'],
        resume=resume_url,
        cover_letter=request.form.get('cover_letter', '')
    )
    
    db.session.add(application)
    db.session.commit()
    
    return redirect(job.company_url)

@app.route('/admin')
def admin_panel():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    applications = Application.query.all()
    return render_template('admin.html', jobs=jobs, applications=applications)

@app.route('/admin/post-job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        image_url = request.form.get('image_url', '')
        
        # Handle file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = url_for('static', filename='uploads/' + filename)
        
        experience = request.form.get('experience', '')
        category = request.form['category']
        
        # Keep original category, fresher jobs will show in both categories
        
        job = Job(
            title=request.form['title'],
            company=request.form['company'],
            category=category,
            description=request.form['description'],
            skills=request.form['skills'],
            location=request.form.get('location', ''),
            salary=request.form.get('salary', ''),
            experience=experience,
            company_url=request.form['company_url'],
            image_url=image_url
        )
        
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!')
        return redirect(url_for('admin_panel'))
    
    return render_template('post_job.html')

@app.route('/admin/applications')
def view_applications():
    applications = Application.query.join(Job).order_by(Application.applied_at.desc()).all()
    return render_template('applications.html', applications=applications)

@app.route('/admin/applications/<int:job_id>')
def job_applications(job_id):
    job = Job.query.get_or_404(job_id)
    applications = Application.query.filter_by(job_id=job_id).order_by(Application.applied_at.desc()).all()
    return render_template('job_applications.html', job=job, applications=applications)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
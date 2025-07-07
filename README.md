# Job Portal Web Application

A complete job portal web application built with Flask and PostgreSQL.

## Features

- **Public Features:**
  - Browse all jobs on home page
  - Filter jobs by categories (IT, Non-IT, Government, Fresher, Internship, Remote, Experienced, Hackathons, Trainee, Guides)
  - View detailed job descriptions with company information and required skills
  - Apply for jobs through popup form
  - Automatic redirection to company website after application

- **Admin Features:**
  - Post new jobs with detailed information
  - View all posted jobs
  - View applications for each job
  - Copy job descriptions from company websites

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup PostgreSQL Database
1. Install PostgreSQL
2. Create a database named `job_portal`
3. Update database credentials in `.env` file

### 3. Environment Configuration
1. Copy `.env.example` to `.env`
2. Update the following variables:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://username:password@localhost/job_portal
   ```

### 4. Initialize Database
```bash
python app.py
```
The database tables will be created automatically on first run.

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` to access the application.

## Usage

### For Job Seekers:
1. Visit the home page to see all available jobs
2. Use the navigation menu to filter jobs by category
3. Click "View Details" to see full job information
4. Click "Apply Now" to submit your application
5. Fill out the application form and submit
6. You'll be redirected to the company's job posting page

### For Administrators:
1. Visit `/admin` to access the admin panel
2. Click "Post New Job" to add a new job posting
3. Fill out all job details including company URL for redirection
4. Use "Copy from Company Job Post" to easily copy job descriptions
5. View applications by clicking on application counts
6. Monitor all applications from the applications page

## Database Schema

### Jobs Table
- id, title, company, category, description, skills, location, salary, company_url, created_at

### Applications Table
- id, job_id, name, email, phone, resume, cover_letter, applied_at

## Categories
- IT
- Non-IT
- Government Jobs
- Fresher
- Internship
- Remote
- Experienced
- Hackathons
- Trainee
- Guides

## Technology Stack
- **Backend:** Flask, SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Styling:** Custom CSS with responsive design
#!/bin/bash
# GoDaddy VPS Deployment Script

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and PostgreSQL
sudo apt install python3 python3-pip postgresql postgresql-contrib nginx -y

# Setup PostgreSQL
sudo -u postgres createdb job_portal
sudo -u postgres createuser job_portal_user
sudo -u postgres psql -c "ALTER USER job_portal_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE job_portal TO job_portal_user;"

# Install app dependencies
pip3 install -r requirements.txt

# Setup Nginx
sudo tee /etc/nginx/sites-available/job_portal << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/job_portal /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Start app
export DATABASE_URL="postgresql://job_portal_user:your_password@localhost/job_portal"
export SECRET_KEY="your-secret-key"
python3 app.py
# CredResolve AI - Deployment Guide

## Overview

This guide provides instructions for deploying the CredResolve AI Debt Collection Agent to production environments.

## Prerequisites

- Python 3.12+
- Node.js 18+
- Gemini API Key
- Domain name (for production)
- SSL certificate (for production)

## Development Deployment

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_api_key_here

# Run development server
python -m app.main
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on `http://localhost:3000`

## Production Deployment

### Backend Deployment

#### Option 1: Traditional VPS (AWS EC2, DigitalOcean, etc.)

1. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip -y

# Install Nginx
sudo apt install nginx -y

# Install SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
```

2. **Deploy Application**
```bash
# Clone repository
git clone <your-repo-url>
cd credresolve/backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/credresolve.service
```

3. **Systemd Service**
```ini
[Unit]
Description=CredResolve Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/credresolve/backend
Environment="PATH=/path/to/credresolve/backend/venv/bin"
Environment="GEMINI_API_KEY=your_api_key_here"
ExecStart=/path/to/credresolve/backend/venv/bin/gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

4. **Start Service**
```bash
sudo systemctl enable credresolve
sudo systemctl start credresolve
sudo systemctl status credresolve
```

5. **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

6. **SSL Configuration**
```bash
sudo certbot --nginx -d api.yourdomain.com
```

#### Option 2: Docker Deployment

1. **Create Dockerfile**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--workers", "4", "--bind", "0.0.0.0:8000"]
```

2. **Build and Run**
```bash
docker build -t credresolve-backend .
docker run -d -p 8000:8000 --env GEMINI_API_KEY=your_key credresolve-backend
```

#### Option 3: Cloud Services (AWS Lambda, Google Cloud Functions)

Convert FastAPI to serverless function using Mangum:

```python
# In main.py
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
```

Deploy using serverless framework or cloud-specific tools.

### Frontend Deployment

#### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel
```

3. **Configure Environment Variables**
```bash
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://api.yourdomain.com
```

4. **Update API Configuration**
In `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```

#### Option 2: Netlify

1. **Build**
```bash
cd frontend
npm run build
```

2. **Deploy**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

3. **Configure Redirects**
Create `netlify.toml`:
```toml
[[redirects]]
  from = "/api/*"
  to = "https://api.yourdomain.com/:splat"
  status = 200
```

#### Option 3: Traditional VPS with Nginx

1. **Build**
```bash
cd frontend
npm run build
```

2. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name app.yourdomain.com;

    root /path/to/credresolve/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **SSL**
```bash
sudo certbot --nginx -d app.yourdomain.com
```

## Environment Variables

### Backend (.env)
```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:password@localhost/credresolve
CHROMA_PERSIST_DIR=/var/lib/chroma_db
```

### Frontend (.env)
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Database Migration

### From SQLite to PostgreSQL

1. **Install PostgreSQL**
```bash
sudo apt install postgresql postgresql-contrib -y
```

2. **Create Database**
```sql
sudo -u postgres psql
CREATE DATABASE credresolve;
CREATE USER credresolve_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE credresolve TO credresolve_user;
\q
```

3. **Update Config**
In `backend/app/config.py`:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://credresolve_user:secure_password@localhost/credresolve")
```

4. **Migrate Data**
Use a migration tool or script to transfer SQLite data to PostgreSQL.

## Monitoring Setup

### Option 1: Built-in Metrics
- Use `/metrics` endpoint
- Build custom dashboard
- Log to file or database

### Option 2: Prometheus + Grafana

1. **Install Prometheus**
```bash
sudo apt install prometheus -y
```

2. **Configure Prometheus**
```yaml
scrape_configs:
  - job_name: 'credresolve'
    static_configs:
      - targets: ['localhost:8000']
```

3. **Install Grafana**
```bash
sudo apt install grafana -y
```

4. **Configure Dashboard**
- Add Prometheus data source
- Create custom dashboards
- Set up alerts

### Option 3: Cloud Monitoring

- AWS CloudWatch
- Google Cloud Monitoring
- Datadog
- New Relic

## Security Hardening

### Backend Security

1. **API Key Protection**
   - Never commit API keys
   - Use environment variables
   - Rotate keys regularly

2. **CORS Configuration**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

3. **Rate Limiting**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    ...
```

4. **Input Validation**
- Use Pydantic models
- Sanitize all inputs
- Validate phone numbers

### Frontend Security

1. **HTTPS Only**
- Force HTTPS in production
- Use secure cookies
- Implement CSP headers

2. **Environment Variables**
- Never expose API keys in client code
- Use build-time variables
- Validate on backend

3. **Authentication** (Future)
- Implement JWT tokens
- Secure session management
- Role-based access control

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**
- Use Nginx or HAProxy
- Distribute traffic across instances
- Health checks

2. **Multiple Backend Instances**
```bash
# Run multiple Gunicorn workers
gunicorn app.main:app --workers 8 --bind 0.0.0.0:8000
```

3. **Database Scaling**
- Use connection pooling
- Implement read replicas
- Consider managed database

### Vertical Scaling

1. **Increase Resources**
- More CPU cores
- More RAM
- Faster storage

2. **Optimize Performance**
- Use caching (Redis)
- Optimize database queries
- Use CDN for static assets

## Backup Strategy

### Database Backup
```bash
# PostgreSQL backup
pg_dump -U credresolve_user credresolve > backup.sql

# SQLite backup
cp credresolve.db credresolve.db.backup
```

### Automated Backup
```bash
# Cron job
0 2 * * * pg_dump -U credresolve_user credresolve > /backups/credresolve_$(date +\%Y\%m\%d).sql
```

### Knowledge Base Backup
```bash
# Backup ChromaDB
tar -czf chroma_backup.tar.gz chroma_db/
```

## Troubleshooting

### Common Issues

1. **Backend Not Starting**
   - Check port availability
   - Verify environment variables
   - Check logs: `journalctl -u credresolve`

2. **Frontend API Errors**
   - Verify API URL
   - Check CORS configuration
   - Inspect browser console

3. **Memory Issues**
   - Increase server RAM
   - Optimize database queries
   - Implement caching

4. **Slow Performance**
   - Add more workers
   - Use CDN
   - Optimize database

## Maintenance

### Regular Tasks

1. **Weekly**
   - Check logs for errors
   - Review metrics
   - Update dependencies

2. **Monthly**
   - Security updates
   - Database backup verification
   - Performance review

3. **Quarterly**
   - Full system audit
   - Capacity planning
   - Cost optimization

## Cost Estimation

### Minimum VPS
- CPU: 2 cores
- RAM: 4GB
- Storage: 40GB SSD
- Cost: ~$20/month

### Recommended Production
- CPU: 4 cores
- RAM: 8GB
- Storage: 80GB SSD
- Cost: ~$40/month

### High Availability
- Load balancer
- 2+ backend instances
- Managed database
- CDN
- Cost: ~$100+/month

## Support

For deployment issues:
1. Check logs
2. Review documentation
3. Consult community forums
4. Contact support team

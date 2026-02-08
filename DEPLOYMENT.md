# 🚀 Deployment Guide

## Free Deployment Options

### 🎨 Frontend Deployment

#### **Option 1: Vercel (Recommended)**
```bash
cd frontend
npm install -g vercel
vercel --prod
```

**Benefits:**
- ✅ 100GB bandwidth/month (free)
- ✅ Automatic deployments from Git
- ✅ Custom domain support
- ✅ HTTPS included
- ✅ Zero configuration needed

#### **Option 2: Netlify**
```bash
cd frontend
npm run build
# Upload the `out` folder to Netlify dashboard
```

#### **Option 3: GitHub Pages**
```bash
# Update package.json homepage
npm run build
# Deploy `out` folder to gh-pages branch
```

### 🔧 Backend Deployment

#### **Option 1: Railway (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy backend
cd backend
railway login
railway up
```

**Benefits:**
- ✅ $5 credit/month (free tier)
- ✅ Python 3.14 support
- ✅ Environment variables
- ✅ Custom domain
- ✅ Auto-deploy from Git

#### **Option 2: Render**
```bash
# Push to GitHub, then connect to Render
# Uses render.yaml configuration
```

#### **Option 3: PythonAnywhere**
```bash
# Upload backend files via web interface
# Configure Python 3.14 web app
```

## 📋 Quick Deployment Steps

### 1. Prepare for Deployment

**Frontend:**
```bash
cd frontend
npm install
npm run build
```

**Backend:**
```bash
cd backend
# Ensure requirements-simple.txt is used
# Update CORS origins for production
```

### 2. Deploy Frontend (Vercel)

```bash
cd frontend
vercel --prod
# Follow prompts, connect to GitHub
```

### 3. Deploy Backend (Railway)

```bash
cd backend
railway login
railway up
# Set environment variables in Railway dashboard
```

### 4. Update API URLs

After deployment, update frontend API calls:
```javascript
// In frontend components
const API_BASE_URL = 'https://your-backend-url.railway.app';
```

## 🔗 Connecting Frontend & Backend

### Production CORS Update
Update `main_fixed.py`:
```python
allow_origins=[
    "https://your-frontend.vercel.app",
    "https://your-domain.com"
]
```

### Environment Variables
Set these in your hosting platform:
```env
NODE_ENV=production
API_BASE_URL=https://your-backend-url.railway.app
```

## 📱 Monitoring

### Free Tier Limits
- **Vercel**: 100GB bandwidth/month
- **Railway**: $5 credit/month (~500 hours runtime)
- **Render**: 750 hours/month

### Monitoring Tools
- Vercel Analytics
- Railway Logs
- Render Metrics

## 🔄 CI/CD Setup

### GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
```

## 🎯 Production Checklist

- [ ] Update CORS origins for production domains
- [ ] Set environment variables
- [ ] Test API endpoints
- [ ] Verify frontend-backend connection
- [ ] Monitor usage limits
- [ ] Set up custom domains (optional)

## 🆘 Troubleshooting

### Common Issues:
1. **CORS errors**: Update allowed origins
2. **API timeouts**: Check hosting limits
3. **Build failures**: Verify dependencies
4. **Connection issues**: Check API URLs

### Support:
- Vercel: https://vercel.com/support
- Railway: https://railway.app/support
- Render: https://render.com/support

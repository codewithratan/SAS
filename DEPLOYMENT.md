# Deployment Guide - Solar Saarthi (Harkrishan Gallery and Services)

## 🚀 Quick Deploy to Render

### Step 1: Prepare Your Repository

1. **Initialize Git (if not already done)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for deployment"
   ```

2. **Create a GitHub Repository**
   - Go to https://github.com/new
   - Create a new repository (e.g., `solar-saarthi`)
   - Don't initialize with README (we already have one)

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/solar-saarthi.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

#### Option A: Blueprint Deployment (Recommended - Easiest)

1. Go to https://render.com and sign up/login
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select your `solar-saarthi` repository
5. Render will detect the `render.yaml` file automatically
6. Click **"Apply"** to create:
   - Web Service (Flask app)
   - PostgreSQL Database
7. Wait 5-10 minutes for deployment to complete
8. Your app will be live at: `https://solar-saarthi.onrender.com`

#### Option B: Manual Deployment

1. **Create PostgreSQL Database**
   - Click **"New +"** → **"PostgreSQL"**
   - Name: `solar-saarthi-db`
   - Region: Choose closest to you
   - Plan: Free
   - Click **"Create Database"**
   - Copy the **Internal Database URL**

2. **Create Web Service**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure:
     - **Name**: `solar-saarthi`
     - **Region**: Same as database
     - **Branch**: `main`
     - **Runtime**: `Python 3`
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn run:app`
     - **Plan**: Free

3. **Add Environment Variables**
   - Click **"Environment"** tab
   - Add:
     ```
     FLASK_ENV=production
     SECRET_KEY=<click "Generate" for secure key>
     DATABASE_URL=<paste Internal Database URL from step 1>
     ```

4. **Deploy**
   - Click **"Create Web Service"**
   - Wait for build to complete

### Step 3: Verify Deployment

1. Open your Render dashboard
2. Click on your web service
3. Click the URL at the top (e.g., `https://solar-saarthi.onrender.com`)
4. You should see your application homepage!

## 📝 Post-Deployment

### Accessing Your Application

- **Homepage**: `https://your-app-name.onrender.com`
- **New Customer**: `https://your-app-name.onrender.com/customer/new`
- **New Service Request**: `https://your-app-name.onrender.com/service/new`
- **Search**: `https://your-app-name.onrender.com/search`

### Database Management

The database is automatically initialized with tables during deployment. No manual setup needed!

### Monitoring

- Check logs in Render dashboard under "Logs" tab
- Monitor database usage under PostgreSQL service

## 🔧 Troubleshooting

### Build Fails

**Error**: `Permission denied: ./build.sh`
- **Solution**: The build script should already be executable. If not, run locally:
  ```bash
  chmod +x build.sh
  git add build.sh
  git commit -m "Make build script executable"
  git push
  ```

**Error**: `Module not found`
- **Solution**: Check `requirements.txt` has all dependencies
- Trigger a manual deploy in Render dashboard

### Database Connection Issues

**Error**: `Could not connect to database`
- **Solution**: 
  1. Verify `DATABASE_URL` environment variable is set
  2. Check database is in the same region as web service
  3. Ensure database is running (check Render dashboard)

### Application Crashes

1. Check logs in Render dashboard
2. Look for Python errors
3. Verify all environment variables are set correctly

### Slow First Load

- **This is normal!** Free tier services spin down after 15 minutes of inactivity
- First request after inactivity takes 30-60 seconds to wake up
- Subsequent requests are fast

## 🔄 Updating Your Application

1. Make changes locally
2. Test locally with `python run.py`
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
4. Render automatically deploys the new version!

## 💰 Cost Information

### Free Tier Includes:
- ✅ 750 hours/month of web service
- ✅ PostgreSQL database (90 days, then expires)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Services spin down after 15 min inactivity

### Paid Plans:
- **Starter ($7/month)**: No spin down, better performance
- **PostgreSQL ($7/month)**: Persistent database, no expiration

## 🌐 Custom Domain (Optional)

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. In Render dashboard, go to your web service
3. Click **"Settings"** → **"Custom Domain"**
4. Add your domain and follow DNS instructions
5. Render provides free SSL certificate!

## 🔐 Security Recommendations

1. **Change SECRET_KEY**: Use Render's "Generate" button for production
2. **Environment Variables**: Never commit `.env` file to Git
3. **Database Backups**: Enable in PostgreSQL settings (paid feature)
4. **HTTPS**: Automatically enabled by Render

## 📊 Alternative Deployment Options

If Render doesn't work for you:

### Railway.app
- Similar to Render
- $5 free credit monthly
- Deploy: https://railway.app

### PythonAnywhere
- Free tier available
- Manual setup required
- Deploy: https://www.pythonanywhere.com

### Heroku
- No longer has free tier
- $7/month minimum
- Deploy: https://www.heroku.com

### DigitalOcean App Platform
- $5/month minimum
- More control
- Deploy: https://www.digitalocean.com/products/app-platform

## 📞 Support

If you encounter issues:
1. Check Render documentation: https://render.com/docs
2. Check application logs in Render dashboard
3. Review this guide's troubleshooting section

---

**Good luck with your deployment! 🎉**

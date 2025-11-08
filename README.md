# Harkrishan Gallery and Services - Service Management System

A comprehensive service management system for Harkrishan Gallery and Services to manage customer service requests, track devices, and generate job cards.

## Features

- **Customer Management**: Add and manage customer information
- **Service Request Tracking**: Create and track service requests for devices
- **Job Card Generation**: Generate professional PDF job cards
- **Search Functionality**: Quickly find customers and service requests
- **Data Export**: Export service records to Excel
- **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd hgs-service-management
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your web browser and go to `http://localhost:5000`

## Usage

1. **Adding a New Customer**
   - Click on "New Customer" in the navigation bar
   - Fill in the customer details and save

2. **Creating a Service Request**
   - Click on "New Service Request"
   - Enter customer ID or search for existing customer
   - Fill in device and service details
   - Save the service request

3. **Generating a Job Card**
   - View the service request details
   - Click on "Generate Job Card" to download a PDF

4. **Searching Records**
   - Use the search functionality to find customers or service requests
   - Search by name, contact number, IMEI, or device details

5. **Exporting Data**
   - Go to the dashboard
   - Click on "Export to Excel" to download all service records

## Project Structure

```
hgs-service-management/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── run.py                 # Application entry point
├── instance/              # Instance folder (created at runtime)
│   └── hgs_service.db     # SQLite database
├── migrations/            # Database migrations (created after initialization)
├── static/                # Static files (CSS, JS, images)
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── customer_form.html # Customer form
    ├── index.html         # Dashboard
    ├── search.html        # Search page
    ├── service_form.html  # Service request form
    └── service_view.html  # Service request details
```

## Deployment to Render

This application is configured for easy deployment to Render.com:

### Prerequisites
- A GitHub account
- A Render account (free tier available at https://render.com)

### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com and sign in
   - Click "New +" and select "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to create both the web service and PostgreSQL database
   - Wait for the build to complete (5-10 minutes)

3. **Access Your Application**
   - Once deployed, Render will provide you with a URL (e.g., `https://solar-saarthi.onrender.com`)
   - Your application will be live and accessible!

### Environment Variables
The following environment variables are automatically configured:
- `FLASK_ENV`: Set to `production`
- `SECRET_KEY`: Auto-generated secure key
- `DATABASE_URL`: Automatically linked to PostgreSQL database

### Important Notes
- **Free tier limitations**: The free tier may spin down after inactivity and take 30-60 seconds to restart
- **Database**: PostgreSQL database is automatically created and linked
- **Migrations**: Database tables are automatically created during deployment

### Alternative: Manual Deployment

If you prefer manual setup:

1. Create a new Web Service on Render
2. Connect your repository
3. Configure:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn run:app`
   - **Environment**: Python 3
4. Add a PostgreSQL database
5. Link the database to your web service

## Local Development

To run locally after deployment setup:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local settings

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the application
python run.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support, please contact the development team.

---

**Harkrishan Gallery and Services** © 2025

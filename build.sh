#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database migrations if not already done
if [ ! -d "migrations" ]; then
    flask db init
fi

# Run migrations
flask db migrate -m "Initial migration"
flask db upgrade

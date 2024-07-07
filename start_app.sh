#!/bin/bash

# Wait for the database to be ready
/app/wait-for-it.sh db:5432 --timeout=15

# Run Alembic migrations
alembic upgrade head

# Prepopulate the database
python prepopulate_db.py

# Start the Uvicorn server
uvicorn src.main:app --host 0.0.0.0 --port 8000
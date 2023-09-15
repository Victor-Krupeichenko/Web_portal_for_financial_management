#!/bin/bash

echo "Waiting..."
sleep 15
alembic upgrade head
echo "FINISH UPGRADE.."
echo "Starting the application on port 5011..."
echo "open application on http://127.0.0.1:5011"
gunicorn app:app --bind=0.0.0.0:5011

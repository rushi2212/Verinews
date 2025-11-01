#!/bin/bash
set -o errexit

cd backend
pip install --no-cache-dir -r requirements.txt

echo "Running database migrations (if any)..."
# Uncomment if you add Alembic later
# alembic upgrade head

echo "Build complete!"

#!/bin/bash -e

# Wait until PostgreSQL is ready
until pg_isready -h 127.0.0.1 -p 5432 -U postgres; do
  echo "Waiting for PostgreSQL database..."
  sleep 1
done

# Move to the application directory
cd /app

# Start the application
exec npm start

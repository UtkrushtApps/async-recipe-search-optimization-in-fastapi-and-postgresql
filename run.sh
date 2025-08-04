#!/bin/bash
set -e
cd /root/task
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker exec recipe_postgres pg_isready -U recipemaster -d recipe_db; do sleep 2; done

# Load schema and data
cat schema.sql | docker exec -i recipe_postgres psql -U recipemaster -d recipe_db
cat data/sample_data.sql | docker exec -i recipe_postgres psql -U recipemaster -d recipe_db

# Check if API is up
echo "Checking if FastAPI service is up..."
for i in {1..10}; do
  if curl -s http://localhost:8000/docs > /dev/null; then
    echo "FastAPI is up!"
    exit 0
  else
    echo "Waiting for FastAPI to start..."
    sleep 2
  fi
done

exit 1

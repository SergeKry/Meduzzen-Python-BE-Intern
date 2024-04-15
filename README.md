# Meduzzen-Python-BE-Intern
## Running the app with Docker:
1. set 'UVICORN_HOST' and "UVICORN_PORT" in the .env file (0.0.0.0:8000 for localhost)
2. set 'DB_NAME', 'DB_USER' and 'DB_PASSWORD' for PostgreSQL database
3. set 'DB_PORT' for PostgreSQL database. Default : 5432 
4. set 'REDIS_PORT'. Default: 6379
5. run 'docker compose build' in terminal
6. run 'docker compose up' in terminal
7. the app is available at 0.0.0.0:8000 by default
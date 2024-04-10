# Meduzzen-Python-BE-Intern
## Running the app directly
1. install dependencies from requirements.txt file:
'pip install -r requirements.txt'
2. Add 'UVICORN_PORT' and 'UVICORN_HOST' to the .env file. Set 'UVICORN_RESTART="True"'for development purposes. (not recommended for production)
3. run the app by executing 'python3 main.py' from the root project folder.

## Running the app with Docker:
1. set 'UVICORN_PORT' and "UVICORN_HOST" in the env.file (0.0.0.0 for localhost)
2. run 'docker compose build' in terminal
3. run 'docker compose up' in terminal
4. the app is available at 0.0.0.0:8000 by default
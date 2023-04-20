# Installation  
1. **Create a virtual environment, install dependencies, create a database:**  
     `python -m venv .venv`  
     `pip install -r requirements.txt`  
     `docker-compose -f docker-compose-local.yaml up -d`  

2. **Creating and applying migrations:**  
**Create an alembic base:**  
`alembic init migrations`  
**Change the path to the database in the alembic file (alembic.ini): **  
`sqlalchemy.url = postgresql://postgres:postgres@0.0.0.0:5432/postgres`  
**Import models into env .py**  
`from main import Base`  
`target_metadata = Base.metadata`  
**Create the first migration**  
`alembic revision --autogenerate -m "comment"`  
**Apply migrations:**  
`alembic upgrade heads`  

3. **Project start:**  
`uvicorn main:app --port 8000 --reload`  

# Project structure:  
**main.py**-- *API routers, and API startup*  
**requirements.txt**-- *project dependencies*  
**session.py** -- *create database session and database engine*  
**settings.py** -- *database and hash settings*  
**security.py**-- *work with tokens*  
**.gitignore** -- *ignore files and folders on commits*  
**docker-compose-local.yaml** -- *docker for db*  
**user/api_login.py** -- *token creation endpoint*  
**user/api** -- *user endpoints*  
**user/dals.py** -- *methods of working with the user through the database*  
**user/hashing.py**-- *password validation and hashing methods*  
**user/models.py** -- *ORM models*  
**user/schemas.py** -- *pydantic models for data validation*  
**user/services.py** -- *service layer (wrappers for database methods,for each method a new session with the database is opened)*

## Flask server demo (tube_tv)

##### Title: Tube_tv
##### Description: tube_tv or netflix clone.
Entities: User, Film, Genre, Actor.

### Getting started

Activate your virtual environment ( on Windows - example)

#### . venv/Scripts/activate 

Install packages:
#### python -m pip install -r requirements.txt


docker commands:
##### 1) docker compose up -d
##### 2) docker compose ps
##### 3) docker compose stop
##### 4) docker compose down (use carefully)
##### 5) docker exec -it pg_container psql


### Create database tube_tv
#### docker exec -i pg_container psql -c 'CREATE DATABASE tube_tv;'

### Generate and insert data into tables ( optional). Run: 
 python seed.py
 
 
### Once the seed.py is ran: 
some lines need to be commented out or uncommented in models.py  to make the attributes related to date as default

Flask commands:
##### 1. flask db migrate
##### 2. flask db upgrade 
##### 3. export FLASK_ENV=development
##### 4. flask run

#### _Work in progress_ ...

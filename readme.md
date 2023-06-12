# To-do list APP

## Description:
**To-do list APP** is a small application for task scheduling. 
App wrote on Django with PostgreSQL.

## Stack:
* Python 3.9
* Django 4.2.2
* PostgreSQL

## How to start:
1) Clone thor repository:    
`git clone https://github.com/bchkrvn/Market-API.git`

2) Create a virtual environment:  
`python -m venv venv`

3) Activate a virtual environment:  
`venv\Scripts\activate.bat`
4) Set up environment variables in the .env file:  
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=skymarket
DB_USER=skymarket
DB_PASSWORD=skymarket
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_PORT=...
DEBUG=1
```

5) Go to the **postgres** folder and run **postgres** with the command:  
`docker-compose up -d`

6) Go to the todolist_app folder and make migrations with the command:  
`python3 manage.py migrate`

7) Run backend with command:  
`python3 manage.py runserver`


## Documentation:
...

## Tests:
...
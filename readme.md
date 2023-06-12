# To-do list APP

## Description:
**To-do list APP** is a small application for task scheduling. 
App wrote on Django with PostgreSQL.

## Stack:
* Python 3.9
* Django 4.2.2
* PostgreSQL

## How to start:
1) Clone this repository:    
`git clone https://github.com/bchkrvn/Market-API.git`

2) Create a virtual environment:  
`python -m venv venv`

3) Activate a virtual environment:  
`venv\Scripts\activate.bat`
4) Set up environment variables in the .env file:  
```
SECRET_KEY='django-insecure-tt6yx98!zil62p7&pv*%q@&!aogyyp#bi)ea3ls8k(cpw4d93#'
DEBUG=1
DB_NAME=todo_list_app
DB_USER=todo_list_app
DB_PASSWORD=todo_list_app
DB_HOST=localhost
DB_PORT=5432
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
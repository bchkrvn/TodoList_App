# To-do list APP

## Description:
**To-do list APP** is a small application for task scheduling. 
App wrote on Django with PostgreSQL.

## Stack:
* Python 3.9
* Django 4.2.2
* DRF
* PostgreSQL
* PyTest

## How to start:
**Server is running on `130.193.53.220`**

*If you want to run local:*
1) Clone this repository:    
`git clone https://github.com/bchkrvn/TodoList_App.git`


2) Go to the **docker** folder and set up environment variables in the **.docker_env** file:  
```
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
SECRET_KEY=...
DEBUG=...
DB_HOST=...
DB_PORT=...
VK_ID=...
VK_SECRET=..
```

3)  Run the project with the command:  
`docker-compose up -d`


## Documentation:
If you want to read documentation, you can find it here: `130.193.53.220/docs/`

## Tests:
If you want to test API, run tests with the command:  
`pytest`
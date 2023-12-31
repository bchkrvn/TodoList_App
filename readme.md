# To-do list APP

## Description:
**To-do list APP** is a small application for task scheduling. 
App wrote on Django with PostgreSQL. Tested with PyTest.

## Stack:
* Python 3.9
* Django 4.2.2
* DRF
* PostgreSQL
* PyTest
* Redis 7.0
* Celery

## Application features:
**Video:**
[![Watch the video](https://img.youtube.com/vi/ZSD_q8A-bYE/maxres3.jpg)](https://youtu.be/ZSD_q8A-bYE)

- Registration, authentication on web-site using VK-account
- Create, update, delete and share boards
- Create, update, delete categories
- Create, update, delete goals
- Watch and create goals using Telegram Bot
- Send messages and email using Celery

## How to start:
**Server is running on http://130.193.53.220**

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
VK_SECRET=...
TGBOT_TOKEN=...
REDIS_HOST=...
REDIS_PORT=...
REDIS_DB=...
EMAIL_HOST=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_PORT=...
```

3)  Run the project with the command:  
`docker-compose up -d`

## Telegram bot:
After registration on the web-site you can use the telegram bot:
http://t.me/TodolistApp_Bot

## Documentation:
If you want to read documentation, you can find it here: http://130.193.53.220/docs/

## Tests:
If you want to test API, run tests with the command:  
`pytest`
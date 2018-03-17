# The battle of the hashtags


## Task description

We would like you to develop a simple application called “The battle of the hashtags”.
The application should allow an administrator to create ‘battles’ between two hashtags,
comparing the number of typos in tweets tagged with them.

A programmatic and automated approach should be used to fetch tweets from the hashtags in
question, on a periodic basis, from the Twitter API.
After a predetermined amount of time, the winning hashtag will be the one with the smallest total
number of typos.

The technical requirements are as follows:
* Python and Django should be used
* Data should be stored on an SQL based datastore
* Security aspects should be taken into consideration
* Delivery needs to happen through a git repository with run instructions
The functional requirements are as follows:
* As an admin, I should be able to use a CRUD to configure battles (Create, Retrieve,
Update, Delete)
* As an admin, I should be able to specify how long a battle will run for, with start and end
date times (please use a datepicker)
* As an admin, I should be able to login/logout

There is no frontend required for this exercise, however, an API endpoint should be exposed to
return the current result for a specific battle id, in JSON format. It should return the battle name,
start and end date times, the hashtags and their number of typos and which one is the winner at
that moment.


## Screenshots


  ![detail1](https://raw.githubusercontent.com/robrechtdr/battle_of_the_hashtags/master/.images/both1.png)

  ![detail2](https://raw.githubusercontent.com/robrechtdr/battle_of_the_hashtags/master/.images/both2.png)

  ![detail3](https://raw.githubusercontent.com/robrechtdr/battle_of_the_hashtags/master/.images/both3.png)

  ![detail4](https://raw.githubusercontent.com/robrechtdr/battle_of_the_hashtags/master/.images/both4.png)

  ![detail5](https://raw.githubusercontent.com/robrechtdr/battle_of_the_hashtags/master/.images/both5.png)

  ![detail6](https://raw.githubusercontent.com/robrechtdr/battle_of_the_hashtags/master/.images/both6.png)

  ![detail7](https://raw.githubusercontent.com/robrechtdr/battle_of_the_hashtags/master/.images/both7.png)



## Setup

> Tested on Ubuntu 16.04

	sudo apt-get install redis-server
	sudo apt-get install redis-tools

	mkvirtualenv battle_of_the_hashtags

	pip install -r requirements.txt

	python manage.py migrate

	python manage.py createsuperuser 


## Run in separate terminal panes

	python manage.py runserver

	celery -A battle_of_the_hashtags worker -l info

	celery -A battle_of_the_hashtags beat -l info


## To check in application

1. Create HashtagBattle entity in `http://localhost:8000/admin`.
2. See battles being triggered in the celery worker pane as they happen (every minute). You can also check the admin or `http://localhost:8000/get_battle/1/`. Not that when outside of start or end date a battle won't be triggered as requested.

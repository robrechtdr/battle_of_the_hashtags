# The battle of the hashtags


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

debug:
	poetry run python manage.py runserver

test:
	poetry run python manage.py test

test-v:
	poetry run python manage.py test -v 1

req:
	poetry export --without-hashes -f requirements.txt -o requirements.txt

wsgi:
	poetry run gunicorn task_manager.wsgi

push:
	git push heroku main

po:
	poetry run python manage.py makemessages -l ru

mo:
	poetry run python manage.py compilemessages -f

shell:
	poetry run python manage.py shell_plus

migrations:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

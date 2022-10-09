debug:
	poetry run python manage.py runserver

req:
	poetry export --without-hashes -f requirements.txt -o requirements.txt

wsgi:
	poetry run gunicorn task_manager.wsgi

push:
	git push heroku main

po:
	poetry run django-admin makemessages -l ru

mo:
	poetry run django-admin compilemessages -f

shell:
	poetry run python manage.py shell_plus

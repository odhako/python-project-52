### Hexlet tests and linter status:
[![Actions Status](https://github.com/odhako/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/odhako/python-project-52/actions)
[![Tests](https://github.com/odhako/python-project-52/actions/workflows/tests.yml/badge.svg)](https://github.com/odhako/python-project-52/actions/workflows/tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/4a9921668f198cad49b7/maintainability)](https://codeclimate.com/github/odhako/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4a9921668f198cad49b7/test_coverage)](https://codeclimate.com/github/odhako/python-project-52/test_coverage)

## Task manager
https://task-manager-by-odhako.up.railway.app/

Task management system. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

### Local installation
Requirements:
```
python ^3.8
poetry ^1.0.0
```
Installation:
```
poetry install
poetry run python manage.py collectstatic
poetry run python manage.py migrate
```
First you need to create superuser:
```
poetry run python manage.py createsuperuser
```

Running server in debug mode:
```
poetry run python manage.py runserver
```
Running server in production mode:
```
poetry run gunicorn task_manager.wsgi
```

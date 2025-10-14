.PHONY: run build migrate superuser test

run:
	python manage.py runserver

build:
	docker-compose build

up:
	docker-compose up

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

superuser:
	python manage.py createsuperuser

test:
	python manage.py test

shell:
	python manage.py shell
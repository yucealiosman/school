build:
	docker-compose build
run:
	docker-compose up

collectstatic:
	docker-compose run web python manage.py collectstatic

makemigrations:
	docker-compose run web python manage.py makemigrations

migrate:
	docker-compose run web python manage.py migrate

user:
	docker-compose run web python manage.py createsuperuser

build_force:
	docker-compose build  --no-cache

test:
	docker-compose run web python manage.py test $(tests)

seed_data:
	docker-compose run web python manage.py seed_data $(student_per_class) $(teacher_count)

run_command:
	docker-compose run web python manage.py $(command)



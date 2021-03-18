## Introduction
This is sample django-rest project for simple school organization


## Running Application
This application is considered to be deployed as a containerized application 
used with Docker. In order to use docker-compose and make, Create a file named .env containing your environment 
variables. env.example file can be used as example.

#### Migrate to database
```
make migrate
```

#### Seed Data
```
make seed_data student_per_class=3 teacher_count=2
```

#### Create superuser
```
make user
```

#### Re-build images
```
make build
```

#### Run server from 8000 port
```
make run
```

#### Usage of pip-tools
```
- pip install pip-tools
- pip-compile requirements.in
- pip install -r requirements.txt
```
If a package is going to be added to the requirements, please add 
it to requirements.in file and then compile it.

If you want to use development environment based requirements
create a file called ```dev-requirements.in``` as an example below then 
compile it 
```pip-compile dev-requirements.in```

```
-r requirements.txt
django-slowtests==1.1.1
ipython==6.3.1
pip-tools==5.1.2
```

Switch between dev and actual requirements
```
pip-sync requirements.txt
pip-sync dev-requirements.txt
```

#### Environment Variables
```
DEBUG
DJANGO_SECRET_KEY
APP_HOST
STATIC_ROOT
POSTGRES_NAME
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
APP_NAME
EMAIL_HOST
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD 
DEFAULT_EMAIL_FROM
CELERY_BROKER_URL
NOTIFY --> Send notifications to student
```
FROM python:3.6.10-alpine3.11 as base

RUN apk update
RUN apk add gcc musl-dev python3-dev postgresql-dev git

ENV PYTHONUNBUFFERED=TRUE

# Creation of the workdir
RUN mkdir /code
ADD requirements.txt /code/

# TODO use multistage approach to reduce image size.
# Install requirements
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
ADD . /code/


WORKDIR /code

FROM python:3.8-alpine

# set work directory
RUN mkdir /code
WORKDIR /code
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev busybox-suid

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy project in work directory
COPY . .
RUN chmod +x manage.py

# for static files
ENV HOME=/code
RUN mkdir $HOME/static

RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

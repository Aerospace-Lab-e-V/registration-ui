FROM python:3.11-alpine

# set work directory
RUN mkdir /code
WORKDIR /code
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade "pip>=26.1.2"
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy project in work directory
COPY . .
RUN chmod +x manage.py

# for static files
ENV HOME=/code
RUN mkdir $HOME/static

RUN addgroup -S app && adduser -S app -G app \
    && chown -R app:app /code

RUN chmod +x /code/entrypoint.sh
USER app
ENTRYPOINT ["/code/entrypoint.sh"]

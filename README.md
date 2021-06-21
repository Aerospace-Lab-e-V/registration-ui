# Registration UI
This is a small tool to handle our project-registrations. Feel free to adapt it to your needs!

## Installation
### Production
Intended for use with reverse proxy (port: 1337)!
- Create `projectSecrets.py` and `.env` by copying the templates
- Fill in all values in `projectSecrets.py` and `.env`
    - DJANGO_ALLOWED_HOSTS are separated by spaces
    - create KEY through: ```py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"```
- ```docker-compose up -d --build```
### Development
- Install requirements: ```pip install -r requirements.txt```
- Initialize DB: ```python manage.py migrate```
- Start local server: ```python ./manage.py runserver```


## Infos
- The website is based on Bootstrap
# Registration UI
## Installation
### Development
#### Install reuquirements:
``` pip install -r requirements.txt ```

#### Initialize DB
``` python manage.py migrate ```

#### Start local server
``` python ./manage.py runserver ```

### Production
Intended for us with Reverseproxy (Port: 1337)!
- create `projectSecrets.py` and `.env` by copying the templates 
- fill in all values in `projectSecrets.py` and `.env`
    - DJANGO_ALLOWED_HOSTS are separated by spaces
    - create KEY through: ```py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"``` 
- ``` docker-compose up -d --build ```


## Infos
- Website based on Bootstrap


# Development
WIP:\
### TODO:
Registriung anmeldedatum -> Reihenfolge

doppelte Mail entfernen?




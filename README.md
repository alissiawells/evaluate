## EvaluateMe
Django application for evaluation output of ML models by humans

### Installation:
* Install Python, Pipenv, Postgres:
```sh
$ git clone https://github.com/alissiawells/evaluate.git
$ cd evaluate
$ virtualenv -p /usr/bin/python3 evaluate
$ source evaluate/bin/activate
$ pip install -r requirements.txt
$ mkdir -p static_cdn
$ mkdir -p media_cdn
```

### Use:

* Make migrations: 
```sh
$ cd src
$ python manage.py migrate
```

* Collect static:
```sh
$ python manage.py collectstatic
```

* Run server on localhost:
```sh
$ python manage.py runserver
```

* Run server on remote machine (in local network):
```sh
$ python manage.py runserver 0.0.0.0:8000
```

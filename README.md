## EvaluateMe
Django application for evaluation output of ML models by humans

### Use

* Make migrations: 
```sh
$ python manage.py makemigrations [APPNAME]
$ python manage.py migrate
```

* Collect static:
```sh
$ python manage.py collectstatic
```

* Populate database with prepared fixture file:
```sh
$ python manage.py loaddata fixture /path/to/fixture/file
```

* Run server on localhost:
```sh
$ python manage.py runserver
```

* Run server on remote machine (in local network):
```sh
$ python manage.py runserver 0.0.0.0:8000
```

### Installation:
* Install Python, Pipenv, Postgres:
```sh
$ git clone https://github.com/alissiawells/evaluate.git
$ cd evaluate
$ conda create -n evaluateme django
$ source activate evaluateme
$ pip install -r requirements.txt
$ mkdir -p static_cdn
$ mkdir -p media_cdn
```

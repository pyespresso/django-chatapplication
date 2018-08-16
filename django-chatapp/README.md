# Django API BoilerPlate
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Django 2.0.7](https://img.shields.io/badge/django%20version-2.0.7-blue.svg)](https://docs.djangoproject.com/en/2.0/releases/2.0.7/)


## Table of Contents
- [Installation](#installation)
   - [Pre Setup Notes](#pre-setup-notes)
   - [Setup Instructions](#setup-instructions)
   - [Warnings](#warnings)
- [Tests](#tests)
   - [Types of tests](#types-of-tests)
   - [Running tests](#running-tests)
   - [Coverage](#coverage)
- [Built With](#built-with)
- [Directory Structure](#directory-structure)


----
## Installation
[(Back to top)](#table-of-contents)

Standard installation as a Django application

### Pre setup notes
The code is compliant with Pylint and pep8, however pylint requires special plugin for Django
and certain warnings/errors have been ignored. Similar for pep8.

To ensure linting is proper, install the required plugins and ensure .pylintrc file is recognized
along with the right Python path. For pep8 setup.cfg file has to be recognized

### Setup Instructions:
- Clone the repo

- ```cd infra```
- ```virtualenv env```
- ```source venv/bin/activate```
- ```pip install -r requirements.txt```
- ```python manage.py runserver```
- (Optional ) To run tests ```python manage.py test --verbosity 3```


----
## Tests
[(Back to top)](#table-of-contents)

### Types of Tests

Python's unittest framework is used for writing all tests. Conventional Django tests module was not used as there was no need to test for views, forms and MVC model specific functionalities.

### Running tests
- Activate the environment
```python
  source venv/bin/activate
```
- In the root dir, write command
```python
  python manage.py test boilerplate -v 3
```

### Coverage

Coverage package is used to generate report on code covered by tests. As only unit testing is done ( i.e. no integration testing ), there are some code lines which aren't tested.

To generate fresh coverage report locally:-

- ```source venv/bin/activate```
- ```bash coverage.sh```

( In terminal there will be output for the coverage of individual files and net coverage )

[Sample Code Coverage](https://github.com/innovaccer/api-boilerplate/wiki/Sample-Code-Coverage)

----
## Built With
[(Back to top)](#table-of-contents)

- Django v2.0.7
- Django REST framework v3.8.2


## Directory structure :
```bash
.
|-- README.md
|-- coverage.sh
|-- docs
|-- infra
|   |-- controllers
|   |   `-- info.py
|   |-- middlewares
|   |   |-- handle_exception.py
|   |   |-- logging.py
|   |   |-- request_validation.py
|   |   `-- resolver.py
|   |-- models
|   |   |-- info.py
|   |   `-- request_validator.py
|   |-- settings.py
|   |-- tests
|   |   `-- test_info.py
|   |-- urls.py
|   |-- utils
|   |   |-- default_model_manager.py
|   |   |-- helpers.py
|   |   |-- http_error.py
|   |   |-- json.py
|   |   |-- loggers
|   |   |   |-- app_logger.py
|   |   |   |-- error_logger.py
|   |   |   |-- logger.py
|   |   |   |-- request_logger.py
|   |   |   `-- response_logger.py
|   |   `-- response.py
|   |-- views
|   |   |-- bad_request.py
|   |   |-- forbidden.py
|   |   |-- internal_server_error.py
|   |   `-- not_found.py
|   `-- wsgi.py
|-- manage.py
|-- requirements.txt
|-- socket_logger.py
|-- static
|-- supervisor
|   `-- socket_logger.pid
`-- templates
```

<!---
[//]: #  command to generate tree. tree -I "venv|*.css|*.pyc|*.js|__init__.py|__pycache__|*.html|*.json|*.png" -C
--->
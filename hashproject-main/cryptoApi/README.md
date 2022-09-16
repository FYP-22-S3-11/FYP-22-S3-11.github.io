
## The first thing to do is to clone the repository:

$ git clone https://github.com/kazmerv/hashproject.git
$ cd hashproject/cryptoApi

## Create a virtual environment to install dependencies in and activate it:

## window mechine refer the following command to setup  virtual environment
$ python -m venv env
$ source env/Scripts/activate

## Then install the dependencies:

(env)$ pip install -r requirements.txt

requirements.txt file content all dependencies that need to install to run the project 

## Run the project 
(env)$ python manage.py runserver

Backend server will run on defult port 8000 http://localhost:8000.

## Run the project on different port 
(env)$ python manage.py runserver 8000

## Deactivate virtual environment
(env)$ deactivate
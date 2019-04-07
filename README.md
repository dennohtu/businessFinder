# businessFinder

[![Build Status](https://travis-ci.org/dennohtu/businessFinder.svg?branch=complete)](https://travis-ci.org/dennohtu/businessFinder)
[![coveralls Analysis](https://coveralls.io/repos/dennohtu/businessFinder/badge.png)](https://coveralls.io/r/dennohtu/businessFinder)

## PRERIQUISITES

A web application that brings businesses and individuals together
A platform that provides business owners to register and display their business profiles to potential customers. 
Customers can log in the application and view a catalogue of registered businesses and be able to give reviews.

## REQUIREMENTS

Python 3.6+(Will not work with python 3.5 and below)

Latest version of pip installed (`sudo apt-get install python3-pip` For python version 3+)

Virtualenv installed (`sudo apt-get install virtualenv`)

PostgreSQL installed on the local machine

## Installing
The following should be done within the project's folder

Create a virtual environment

`python3 -m virtualenv <env-name>`

Activate the virtual environment

`source <env-name>/bin/activate`

Install requirements from requirements.txt

`pip3 install -r requirements.txt`

You need to create a new user in postgreSQL named `admin`.

After creating the new user, enter into your python3 shell and set up with the following:

`import db`
`db.create_all()`


## RUNNING

After activating your virtual environment, start the flask server with

`python3 run.py`

Enjoy :)

Deactivate the virtual environment using

`deactivate`

Live application on heroku

https://business-finder-dennohtu.herokuapp.com/
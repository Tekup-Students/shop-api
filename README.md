## Shop API

## Installation With python virtual environments

# Requirements
python 3.5 or higher;

## Setting the Project Locally:

#### Cloning the project:

Once you have all the needed requirements installed, clone the project:

``` bash
git clone git@github.com:h5llsing/shop-api.git
```


## Create an environment
Create a project folder and a venv folder within:

``` bash
$ python3 -m venv venv
```


# Install dependencies
Now, you will need to set up virtual environment that will keep the application and its dependencies isolated from the main system.

Next run the following command with the name of your temporary virtual environment.

``` bash
$ source venv/bin/activate
```

For this project pipenv is used to handle dependencies, here is a quickstart
to install and use _pipenv_, in the following command pipenv is installed 
for the current user, usually under __/home/{user}/.local/bin/pipenv__
``` bash
$ pip install --user pipenv
```

_Note: sometimes __$HOME/.local/bin__ is not in the $PATH you need to add it._

To start use pipenv for a new project, run the following command:
``` bash
$ pipenv install [--python 3.8]
```
A new file _Pipfile_ is created in the current directory and a virtual environment
under __/home/{user}/.local/share/virtualenvs/__ is set.
If you want to specify which python version to use it needs to be installed in
your systeme.


To install a new dependency, note that you need to be in a directory/subdirectory
holding _Pipfile_:
``` bash
$ pipenv install requests
```

To activate the virtual environment, run the following:
``` bash
$ pipenv shell
```
The name of the project is added at the beginning of the prompt to specify which
environment is loaded.

To show installed dependencies, type this command:
``` bash
$ pipenv graph
```

# Usage
There's no need to configure anything to run the application.

Run this command to run the built-in web server and access the application in your browser at http://localhost:5000:

``` bash
$ python3 manage.py runserver
```

## Installation with docker

## Project Requirements:

In order to get the project running you need to install:

- [Docker](https://docs.docker.com/get-docker/).

#### Docker:

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

## Setting the Project Locally:

#### Cloning the project:

Once you have all the needed requirements installed, clone the project:

``` bash
git clone git@github.com:h5llsing/shop-api.git
```

#### Configure .env file:

Before you can run the project you need to set the envirment varibles:

``` bash
$ cp .env.example .env
```

#### Usage:

to run the project type:

``` bash
docker-compose up --build
```

Check 0.0.0.0:3000 on your browser!


That's it.

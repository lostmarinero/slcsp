
# SLCSP Instructions
Thank you for taking the time to review my work. I always appreciate any feedback, if at all possible. 

For this project, Python 3.6.0 was used as it is the latest stable release of Python3.

## Dependencies
To run this script, you only need Python 3.6.0 as there were no external packages (only built in ones). However, for development, I did using the pytest testing framework.

I have included instructions to setting up a virtualenv in case one wants to run the tests using pytest.

#### Required:
* [Python 3.6.0](https://www.python.org/downloads/release/python-360/)

#### Recommended:
* [Pip 9.0.1](https://pip.pypa.io/en/stable/)
* [Pytest 3.0.7](http://doc.pytest.org/en/latest/)
* [pyenv 1.0.8](https://github.com/pyenv/pyenv)
* [pyenv-virtualenv 1.0.0](https://github.com/pyenv/pyenv-virtualenv)

## Install Python 3.6.0
Mac OS X users can install Python 3 directly with [Homebrew](https://brew.sh/) package manager. To install Homebrew, [please see these directions](https://brew.sh/).

To install Python3 with Homebrew, enter:

    $ brew install python3

NOT USING A MAC? To install Python3 on a different system, please see the downloads section of the [Python website](https://www.python.org/downloads/).

* DO NOTE that if you install python through Homebrew, Python 3 is used with the `python3` command. Instead of ` $ python {some command}`, you use ` $ python3 {some command}`.

## Run the Script
To run the script as outlined in the instructions, ensure the virtualenv with python 3.6.0 is activated (`python --version`).

To run the script, from the root directory of 'slcsp', simply enter:

    $ python3 main.py

This will import the slcsp.csv file and output to the exact same file the zip codes with the benchmark rates.

The original slcsp.csv file will be saved as `original_slcsp_{TIMESTAMP}`


# Virtualenv and Testing
To run the tests, we need to install pytest. Pytest is a testing framework that can be installed with pip, the Python package manager.

To ensure we install the correct dependencies for the script, we will create a virtual environment that uses Python 3.6.0 and the dependencies outlined above.

I will describe setting up the virtualenv using pyenv (which allows us to install and set the Python version) and pyenv-virtualenv, which allows us to create a virtualenv with our dependencies.

### Install pyenv
To install pyenv with Homebrew:
    
    $ brew update
    $ brew install pyenv

[Additional installation instructions can be found here](https://github.com/pyenv/pyenv#homebrew-on-mac-os-x)

### Install pyenv-virtualenv
pyenv-virtualenv is a pyenv plugin that provides features to manage virtualenvs with Python. It allows for dependencies to be installed inside virtual environments.

    $ brew install pyenv-virtualenv

Add the following to your `~/.bash_profile` or terminal startup script
    
    $ eval "$(pyenv init -)"
    $ eval "$(pyenv virtualenv-init -)"


### Install Python3
Using pyenv, install Python3

    $ pyenv install 3.6.0


### Create New Virtualenv
Creat a new virtualenv with Python 3.6.0

    $ pyenv virtualenv 3.6.0 slcsp_env

### Activate Virtualenv
Move to the base directory
    
    $ cd {Some/Path}/homework/slcsp

And activate the 'slcsp_env' virtualenv

    $ pyenv activate slcsp_env

### Ensure Pip Latest Version

    $ pip install --upgrade pip

### Install Pytest
The only requirement is pytest (and those required by pytest).

To install, simply enter:

    $ pip install pytest

or run:

    $ pip install -r requirements.txt

Now your environment is ready!

## Run the Tests
Ensure the virtualenv is activated.

To run the written tests with a verbose output, enter:
    
    $ pytest -vs

## Run Script in Virtualenv

To run the slcsp.csv script within the virtualenv, use `python` instead of `python3`
    
    $ python main.py


# Some Notes

I ended up spending more time than expected and writing a full set of tests for this challenge, as I felt it was kind of necessary to fully ensure the reading/writing to csv files was doing everything that I had expected. 

I find that while working with files directly, there can often be issues with the path (especially if you develop the file in one environment and then push it to a staging/production environment), writing issues (such as expecting None to be represented by an empty string but being something else), or errors/typos in the input file/data can cause your script to fail (and therefore the importation has to expect these imperfections).

Full disclosure, I normally try to ensure full coverage of my code with unit and integration tests, though some coding challenges do not allow enough time for implementing test coverage.

I was fortunate to have written these tests, as it helped me discover I had overlooked that a benchmark plan was the second lowest UNIQUE rate 'Silver' plan. I had originally just looked for the second lowest rate plan, but had not considered they had to be unique rates.


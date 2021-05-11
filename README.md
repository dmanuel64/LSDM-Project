# LSDM-Project
CS 4243 - Large-Scale Data Management Spring 2021 Project (Front-End)

## Prerequisites
**Python verson**

This project has been built and tested for Python 3.8.5; other versions may not be compatible. Run ```python3 --version``` to check the python version and see if it is the correct one.


**Optional: Enable a Python venv**

Some of our libraries are pinned to specific versions. This may cause conflicts with other installed applications. To prevent these issues, a Python venv can be enabled to separate the libraries for this project from the rest of the system's libraries.

Assuming the project has been downloaded into PROJECT_DIR, a venv can be created as follows:

```
python3 -m venv $PROJECT_DIR
```

To use the venv, source the venv activation script:

```
source $PROJECT_DIR/bin/activate
```

**Before starting the application, you will need to install prerequisite libaries**

For convenience, the required libraries have been compiled into requirements.txt. Pip can be used to install all prerequisites with either of the following commands:
```
pip3 install -r requirements.txt
python3 -m install -r requirements.txts
```

**Database software**

The Django configuration used in the project uses MongoDB as the database for the backend. This will need to be installed before attempting to run the project. On Ubuntu, this can be installed as follows:

```
sudo apt install mongodb
```

For other platforms, see the MongoDB website or distribution documentation for installation instructions.

## Usage

Run the start_web_app.bash bash script to start the web server:
```
bash start_web_app.bash
```
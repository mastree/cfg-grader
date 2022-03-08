# CFG Grader
Author: Muhammad Kamal Shafi

Grader for Control Flow Graph similarity, calculated using Graph Edit Distance exact calculation with upper bound approximation and time limit.

# Python Dependencies

Required to have python version 3.10 or later (due to type hinting).

## update dependencies
```sh
pip freeze > requirements.txt
```

## install all dependencies
```sh
pip install -r requirements.txt
```

on windows you might encounter problem when installing pygraphviz, you can solve it by informing pip on where is graphviz installed, e.g.
```cmd
python -m pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz
```

# How to Use Virtualenv

## create new virtual env
you only need to do this once
```sh
python3 -m venv .venv
```

## start virtualenv
On linux
```sh
source .venv/bin/activate
```

On windows
```cmd
.venv\Scripts\activate.bat
```

## terminate Virtualenv
```sh
deactivate
```

## Run Project

Run the service by using this command:

```bash
PYTHONPATH=$(pwd) python webservice/src/main.py
```

You can then try to hit the endpoint `localhost:5000/healthcheck` to see if it's working or not.

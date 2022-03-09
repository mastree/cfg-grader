# CFG Grader
**Author: Muhammad Kamal Shafi**

Grader for Control Flow Graph similarity, calculated using Graph Edit Distance exact calculation with upper bound pruning and time limit.

---

# How to Run

## Running on Docker

Luckily, this project does not require many dependencies, so you can simply run this service with [Docker](https://www.docker.com/).

Once you have `docker` and `docker-compose` installed you can simply run this command on your terminal:

```bash
docker-compose up
```

This will build and run the [Dockerfile](./Dockerfile). If no problems were found, you will see this in your terminal:

```bash
...
app_1  |  * Serving Flask app "main" (lazy loading)
app_1  |  * Environment: production
app_1  |    WARNING: This is a development server. Do not use it in a production deployment.
app_1  |    Use a production WSGI server instead.
app_1  |  * Debug mode: off
app_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Note that even though it says `http://0.0.0.0:5000`, the service can only be accessed at `http://127.0.0.1:5000` or `localhost:5000`.

Now you can open `localhost:5000/health-check` to see if it's successfully running or not.

<!-- TODO: Add Documentation on API -->

---

# Running on Local

## How to Use Virtualenv

### Create a New Virtualenv
you only need to do this once
```sh
python3 -m venv .venv
```

### Start Virtualenv
On linux
```sh
source .venv/bin/activate
```

On windows
```cmd
.venv\Scripts\activate.bat
```

### Terminate Virtualenv
```sh
deactivate
```

## Python Dependencies

Required to have **python** version **3.9** or **later**.

### Install All Dependencies
```sh
pip install -r requirements.txt
```

### Update Dependencies
```sh
pip freeze > requirements.txt
```

On windows you might encounter problem when installing pygraphviz, you can solve it by informing pip on where is graphviz installed, e.g.
```cmd
python -m pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz
```

## Run the Projects

Run the service by using this command:

```bash
PYTHONPATH=$(pwd) python webservice/src/main.py
```

You can then try to hit the endpoint `localhost:5000/healthcheck` to see if it's working or not.

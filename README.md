# Common setup

```
$ cp .env.template .env

# Edit the content of `.env` as per the comments/instructions therein.
```

# Options for serving the application and issuing requests to it

1. Using Docker to serve the persistence layer, but locally serving the Flask application:

    ```
    $ python3 --version
    Python 3.8.3

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```

    ```
    docker run \
        --name container-microjira-mysql \
        --add-host host.docker.internal:host-gateway \
        --mount source=volume-microjira-mysql,destination=/var/lib/mysql \
        --env-file .env \
        --publish 3307:3306 \
        mysql:8.0.26 \
        --default-authentication-plugin=mysql_native_password
    ```

    ```
    (venv) $ FLASK_APP=application.py flask db upgrade

    (venv) $ ll *.sqlite
    -rw-r--r--  1 <user-owner>  <group-owner>    24K Mar  9 06:53 database.sqlite
    ```

    ```
    # Launch one terminal instance and, in it, start serving the application:

    (venv) $ FLASK_APP=application.py flask run
    ```

    ```
    # Launch a second terminal instance and, in it, issue requests to the application:

    $ curl localhost:5000/api/projects | json_pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100    16  100    16    0     0    106      0 --:--:-- --:--:-- --:--:--   131
    {
      "projects" : []
    }

    $ curl \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"name": "Build a basic web application using Flask"}' \
        localhost:5000/api/projects \
        | json_pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100   113  100    60  100    53    521    460 --:--:-- --:--:-- --:--:--   982
    {
      "id" : 1,
      "name" : "Build a basic web application using Flask"
    }

    $ curl localhost:5000/api/projects | json_pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100    75  100    75    0     0   1975      0 --:--:-- --:--:-- --:--:--  8333
    {
      "projects" : [
          {
            "id" : 1,
            "name" : "Build a basic web application using Flask"
          }
      ]
    }
    ```

2. Using Docker

    ```
    $ docker build --file Dockerfile --tag image-microjira:2022-03-09-07-25 .

    $ docker run \
      --name container-microjira \
      --env-file .env \
      --publish 8000:5000 \
      --rm \
      --detach \
      image-microjira:2022-03-09-07-25
    ```

    ```
    $ curl localhost:8000/api/health-check | json_pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100    26  100    26    0     0    220      0 --:--:-- --:--:-- --:--:--   433
    {
      "health-check" : "passed"
    }

    $ curl localhost:8000/api/projects | json_pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100    16  100    16    0     0    139      0 --:--:-- --:--:-- --:--:--   177
    {
      "projects" : []
    }

    $ curl \
      -X POST \
      -H "Content-Type: application/json" \
      -d '{"name": "Build a basic web application using Flask"}' \
      localhost:8000/api/projects \
      | json_pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100   113  100    60  100    53    642    567 --:--:-- --:--:-- --:--:--  1793
    {
      "id" : 1,
      "name" : "Build a basic web application using Flask"
    }

    $ curl localhost:8000/api/projects | json_pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100    68  100    68    0     0    945      0 --:--:-- --:--:-- --:--:--  2720
    {
      "projects" : [
          {
            "name" : "Build a basic web application using Flask"
          }
      ]
    }
    ```

# Dawdle - API

[![Build Status](https://img.shields.io/github/workflow/status/vanillaSlice/dawdle/Deploy%20API/master)](https://github.com/vanillaSlice/dawdle/actions?query=workflow%3A%22Deploy+API%22+branch%3Amaster)
[![Coverage Status](https://img.shields.io/codecov/c/gh/vanillaSlice/dawdle/master?flag=api)](https://codecov.io/gh/vanillaSlice/dawdle/branch/master)

The Dawdle API.

A deployed version can be viewed [here](https://dawdle-api.mikelowe.xyz/) (it's running on Heroku so may take a moment
to wake up).

## Configuration

The following properties can be configured:

| Name                    | Purpose                                                          | Default               |
| ----------------------- | ---------------------------------------------------------------- | --------------------- |
| `DEBUG`                 | If debug mode is enabled.                                        | `False`               |
| `ENV`                   | Environment the app is running in.                               | `production`          |
| `SECRET_KEY`            | A secret key used for security.                                  | `default secret key`  |
| `SERVER_NAME`           | The host and port of the server.                                 | `127.0.0.1:5000`      |
| `SESSION_COOKIE_DOMAIN` | The domain match rule that the session cookie will be valid for. | `127.0.0.1:5000`      |

To change these properties you can export them as environment variables or create a file `instance/config.py` (note
that environment variables take precedence).

## Running

The app can be run [with Docker](#with-docker) or [without Docker](#without-docker).

#### With Docker

From your terminal/command prompt run:

```
docker-compose up
```

Then point your browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

#### Without Docker

From your terminal/command prompt run:

```
pip install -r requirements.txt
./run.py
```

Then point your browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

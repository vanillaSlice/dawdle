# Dawdle - API

[![Build Status](https://github.com/vanillaSlice/dawdle/workflows/Build%20API/badge.svg?branch=master)](https://github.com/vanillaSlice/dawdle/actions?query=workflow%3A%22Build+API%22+branch%3Amaster)
[![Deploy Status](https://github.com/vanillaSlice/dawdle/workflows/Deploy%20API/badge.svg?branch=master)](https://github.com/vanillaSlice/dawdle/actions?query=workflow%3A%22Deploy+API%22+branch%3Amaster)
[![Coverage](https://codecov.io/gh/vanillaSlice/dawdle/branch/master/graph/badge.svg?flag=api)](https://codecov.io/gh/vanillaSlice/dawdle/branch/master)

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

TODO

#### Without Docker

##### Installing Requirements

1. (Optional) Install [virtualenv](https://pypi.org/project/virtualenv/) and
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) and create a new environment.
2. Run `pip install -r requirements.txt`.

##### Running

From your terminal/command prompt run:

```
./run.py
```

# Dawdle

[![Latest Release](https://img.shields.io/github/release/vanillaSlice/dawdle.svg)](https://github.com/vanillaSlice/dawdle/releases/latest)
[![Build Status](https://img.shields.io/travis/com/vanillaSlice/dawdle/master.svg)](https://travis-ci.com/vanillaSlice/dawdle)
[![Coverage Status](https://img.shields.io/coveralls/github/vanillaSlice/dawdle/master.svg)](https://coveralls.io/github/vanillaSlice/dawdle?branch=master)
[![License](https://img.shields.io/github/license/vanillaSlice/dawdle.svg)](LICENSE)

A [Trello](https://trello.com/) clone built with [Flask](http://flask.pocoo.org/).
A deployed version can be viewed [here](https://dawdle.mikelowe.xyz/).

## Screenshot

TODO

## Getting Started

* [With Docker](#with-docker)
* [Without Docker](#without-docker)

### With Docker

#### Prerequisites

* [Docker](https://www.docker.com/)

#### Running

From your terminal/command prompt run:

```
docker-compose up
```

Then point your browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

### Without Docker

#### Installing Requirements

1. (Optional) Install [virtualenv](https://pypi.org/project/virtualenv/) and
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) and create a new environment.
2. Run `pip install -r requirements.txt`.

#### Setting up MongoDB

You can either:

* Install MongoDB locally by going [here](https://www.mongodb.com/download-center#community).

or:

* Create a database in the cloud using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

#### Configuration

The following properties can be configured:

| Name                    | Purpose                                                          | Default              |
| ----------------------- | ---------------------------------------------------------------- | -------------------- |
| `DEBUG`                 | If debug mode is enabled.                                        | `False`              |
| `ENV`                   | Environment the app is running in.                               | `production`         |
| `MAIL_DEFAULT_SENDER`   | The default address to send emails from.                         | `None`               |
| `MAIL_PASSWORD`         | The mail sender's password.                                      | `None`               |
| `MAIL_PORT`             | The mail server port.                                            | `25`                 |
| `MAIL_SERVER`           | The mail server host name.                                       | `127.0.0.1`          |
| `MAIL_SUPPRESS_SEND`    | If mail sending should be suppressed.                            | `False`              |
| `MAIL_USE_SSL`          | If using mail SSL.                                               | `False`              |
| `MAIL_USE_TLS`          | If using mail TLS.                                               | `False`              |
| `MAIL_USERNAME`         | The mail sender's username.                                      | `None`               |
| `MONGODB_DB`            | The MongoDB database name.                                       | `dawdle`             |
| `MONGODB_HOST`          | The MongoDB host name.                                           | `127.0.0.1`          |
| `MONGODB_PASSWORD`      | The MongoDB password.                                            | `None`               |
| `MONGODB_PORT`          | The MongoDB port.                                                | `27017`              |
| `MONGODB_USERNAME`      | The MongoDB username.                                            | `None`               |
| `SECRET_KEY`            | A secret key used for security.                                  | `default secret key` |
| `SERVER_NAME`           | The host and port of the server.                                 | `127.0.0.1:5000`     |
| `SESSION_COOKIE_DOMAIN` | The domain match rule that the session cookie will be valid for. | `127.0.0.1:5000`     |
| `WTF_CSRF_ENABLED`      | If CSRF protection is enabled.                                   | `True`               |

To change these properties you can export them as environment variables or create a file `instance/config.py` (note
that any environment variables take precedence).

URI style connections are also supported for connecting to MongoDB, just supply the URI as `MONGODB_HOST` (note that
URI properties will take precedence).

#### Running

From your terminal/command prompt run:

```
./run.py
```

Then point your browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Technology Used

For those of you that are interested, the technology used in this project includes:

* [Python 3.7](https://www.python.org/downloads/release/python-373/)
* [Flask](http://flask.pocoo.org/) (Microframework)
* [MongoDB](https://www.mongodb.com/) and
[Flask-MongoEngine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/) (Database)
* [pytest](https://docs.pytest.org/en/latest/) and [Mongomock](https://github.com/mongomock/mongomock) (Testing)
* [Docker](https://www.docker.com/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

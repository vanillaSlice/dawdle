FROM python:3.9.1-alpine
WORKDIR /opt/app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./dawdle ./dawdle
COPY ./config.py ./config.py
COPY ./run.py ./run.py
COPY ./docs/api.yml ./docs/api.yml
CMD gunicorn --bind=0.0.0.0:8000 --workers=4 --reload --preload run:app

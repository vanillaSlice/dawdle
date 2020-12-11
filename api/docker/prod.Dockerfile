FROM python:3.9.1-alpine
WORKDIR /opt/app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN rm ./requirements.txt
COPY ./dawdle ./dawdle
COPY ./config.py ./config.py
COPY ./run.py ./run.py
COPY ./docs/api.yml ./docs/api.yml
CMD gunicorn --workers=4 --preload run:app

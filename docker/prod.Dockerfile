FROM python:3.7.3-alpine

WORKDIR /opt/app

# Install the requirements
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN rm ./requirements.txt

# Copy the code
COPY ./dawdle ./dawdle
COPY ./config.py ./config.py
COPY ./run.py ./run.py

# Run the app
CMD gunicorn --workers=4 run:app

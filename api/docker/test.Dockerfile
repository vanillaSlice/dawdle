FROM python:3.9.1-alpine
RUN apk update && apk upgrade && apk add bash
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt
RUN pip install -r requirements-test.txt
CMD ./scripts/local/tests.sh

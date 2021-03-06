FROM python:3.8.4-alpine
RUN apk update && apk upgrade && apk add bash
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt
RUN pip install -r requirements-test.txt
CMD ./scripts/all-tests.sh

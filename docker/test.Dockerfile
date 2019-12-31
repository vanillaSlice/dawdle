FROM python:3.8.1-alpine
RUN apk update && apk upgrade && apk add bash && apk add git
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt
RUN pip install -r requirements-test.txt
CMD ./scripts/lint.sh && ./scripts/test.sh

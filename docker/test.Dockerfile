FROM python:3.8.1-alpine
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt
RUN pip install -r requirements-test.txt
CMD ./scripts/lint.sh && ./scripts/test.sh
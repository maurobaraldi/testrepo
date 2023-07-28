FROM python:3.11-alpine3.17

WORKDIR /var/app

COPY . /var/app/
RUN /usr/bin/crontab /var/app/crontab.txt
RUN apk add git
RUN pip install jinja2

ENTRYPOINT ["python /var/app/generator.py"]

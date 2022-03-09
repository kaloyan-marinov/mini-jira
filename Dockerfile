FROM python:3.8.3-alpine

# https://github.com/python-greenlet/greenlet/issues/232#issuecomment-910128433
RUN apk add build-base

RUN adduser -D the-mighty-user

WORKDIR /home/the-mighty-user

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY migrations migrations
COPY application.py ./

COPY boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP application.py

RUN chown -R the-mighty-user:the-mighty-user ./
USER the-mighty-user

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

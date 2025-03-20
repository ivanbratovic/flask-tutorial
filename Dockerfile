FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

RUN mkdir -p /blog
WORKDIR /blog

COPY app app
COPY migrations migrations
COPY blog.py config.py entrypoint.sh ./
RUN chmod a+x entrypoint.sh

ENV FLASK_APP blog.py
RUN flask translate compile

EXPOSE 5000
ENTRYPOINT ["/blog/entrypoint.sh"]

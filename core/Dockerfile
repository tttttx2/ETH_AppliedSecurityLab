FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ssl.conf /etc/nginx/conf.d/ssl.conf
COPY ./ssl/* /etc/nginx/

COPY ./app /app
COPY ./openssl.cnf /etc/ssl/openssl.cnf

COPY imovies_internal.crt /usr/local/share/ca-certificates/imovies_internal.crt
RUN chmod 644 /usr/local/share/ca-certificates/imovies_internal.crt
RUN cat /usr/local/share/ca-certificates/imovies_internal.crt >> /etc/ssl/certs/ca-certificates.crt
RUN update-ca-certificates

RUN pip install pyjwt
RUN pip install mysql-connector-python
RUN pip install requests

RUN apt update
RUN apt install -y rsyslog default-mysql-client cron docker docker-compose

COPY ./rsyslog.conf /etc/rsyslog.conf

RUN rm /var/log/nginx/access.log
RUN rm /var/log/nginx/error.log
RUN touch /var/log/nginx/access.log
RUN touch /var/log/nginx/error.log

RUN touch /var/log/application.log




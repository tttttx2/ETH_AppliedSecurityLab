FROM nginx

COPY ./default.conf /etc/nginx/conf.d/default.conf

COPY ./html/* /var/www/html/

COPY ./includes/ /etc/nginx/includes/

COPY ./ssl/ /etc/ssl/certs/nginx/

COPY imovies_internal.crt /usr/local/share/ca-certificates/imovies_internal.crt
RUN chmod 644 /usr/local/share/ca-certificates/imovies_internal.crt
RUN cat /usr/local/share/ca-certificates/imovies_internal.crt >> /etc/ssl/certs/ca-certificates.crt
RUN update-ca-certificates


RUN apt update
RUN apt install -y rsyslog
COPY ./rsyslog.conf /etc/rsyslog.conf

RUN touch /var/log/nginx/nostd.access.log
RUN touch /var/log/nginx/nostd.error.log

COPY 90_start_rsyslog.sh /docker-entrypoint.d
COPY htpasswd /.htpasswd
#RUN ["service", "rsyslog", "start"]
#ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]

FROM mariadb:latest

ENV MYSQL_ROOT_PASSWORD='No9fohe6aejo9Ohfof6d'
ENV MYSQL_USER='root2'
ENV MYSQL_PASSWORD='chiMi8axaitheivoo3oh'
ENV MYSQL_DATABASE='db'
#ENV MYSQL_ROOT_HOST='10.0.0.30'

COPY ./dump/* /docker-entrypoint-initdb.d/


# NO SSL CONFIG YET
#COPY ./10-ssl.cnf /etc/mysql/conf.d/10-ssl.cnf
#COPY ./imovies_internal.crt /etc/mysql/cacert.pem
#COPY ./ssl/*.key /etc/mysql/server-key.pem
#COPY ./ssl/*.crt /etc/mysql/server-cert.pem

RUN apt update
RUN apt install -y rsyslog
COPY ./rsyslog.conf /etc/rsyslog.conf

COPY ./prestart.sh /prestart.sh
RUN cp /usr/local/bin/docker-entrypoint.sh /docker-entrypoint.sh
RUN cat /prestart.sh /docker-entrypoint.sh > /usr/local/bin/docker-entrypoint.sh

FROM rsyslog/syslog_appliance_alpine:latest

RUN apk add --update bash

RUN apk add ca-certificates logrotate
COPY imovies_internal.crt /usr/local/share/ca-certificates/imovies_internal.crt
RUN chmod 644 /usr/local/share/ca-certificates/imovies_internal.crt
RUN cat /usr/local/share/ca-certificates/imovies_internal.crt >> /etc/ssl/certs/ca-certificates.crt
RUN update-ca-certificates

COPY logrotate_rsyslog /etc/logrotate.d/rsyslog_custom
COPY rsyslog_log_to_files.conf /etc/rsyslog.conf.d/log_to_files.conf



CMD ["rsyslog"]


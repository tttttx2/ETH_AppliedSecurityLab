FROM alpine:latest

COPY ./app /app
RUN chmod +x /app/main.sh

RUN apk add --update bash

RUN apk add ca-certificates
COPY imovies_internal.crt /usr/local/share/ca-certificates/imovies_internal.crt
RUN chmod 644 /usr/local/share/ca-certificates/imovies_internal.crt
RUN cat /usr/local/share/ca-certificates/imovies_internal.crt >> /etc/ssl/certs/ca-certificates.crt
RUN update-ca-certificates


CMD ["sh", "app/main.sh"]


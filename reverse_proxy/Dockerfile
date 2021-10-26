FROM nginx

COPY ./default.conf /etc/nginx/conf.d/default.conf

COPY ./html/* /var/www/html/

COPY ./includes/ /etc/nginx/includes/

COPY ./ssl/ /etc/ssl/certs/nginx/

COPY imovies_internal.crt /usr/local/share/ca-certificates/imovies_internal.crt
RUN chmod 644 /usr/local/share/ca-certificates/imovies_internal.crt
RUN cat /usr/local/share/ca-certificates/imovies_internal.crt >> /etc/ssl/certs/ca-certificates.crt
RUN update-ca-certificates

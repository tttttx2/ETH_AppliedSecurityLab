# initial creation of  ca
```
# ohpe3yoo3Oap5dohsahya1eeBieweehohseitaet
openssl genrsa -des3 -out myCA.key 2048
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem
```

# create CRL
```
echo "00" > /data/myCA.crl
openssl ca -config /etc/ssl/openssl.cnf -gencrl -out /data/crl.pem -passin pass:ohpe3yoo3Oap5dohsahya1eeBieweehohseitaet # must be done after revoking again
```

# create client CSR and key
https://jamielinux.com/docs/openssl-certificate-authority/certificate-revocation-lists.html

```
NAME=asdf
openssl req -new -nodes -sha256 -newkey rsa:2048 -keyout $NAME.key -out $NAME.csr -subj "/emailAddress=webmaster@example.com/CN=example.com/O=imovies email/OU=iMovies email/C=CH/ST=Zuerich/L=Zuerich"
# openssl x509 -req -days 365 -in $NAME.csr -CA /data/myCA.pem -CAkey /data/myCA.key -out $NAME.crt -CAserial /data/srlnumber -passin pass:ohpe3yoo3Oap5dohsahya1eeBieweehohseitaet # -CAcreateserial 
openssl ca -config /etc/ssl/openssl.cnf -extensions usr_cert -notext -md sha256 -in $NAME.csr -out $NAME.crt -passin pass:ohpe3yoo3Oap5dohsahya1eeBieweehohseitaet
openssl pkcs12 -export -in $NAME.crt -inkey $NAME.key -out $NAME.pfx -passout pass:
```

# revoke cert
```
openssl ca -config /etc/ssl/openssl.cnf -revoke 1145DBBD8B4FD383C925440017931D124E07169C.pem -passin pass:ohpe3yoo3Oap5dohsahya1eeBieweehohseitaet
# regenerate crl 
openssl ca -config /etc/ssl/openssl.cnf -gencrl -out /data/crl.pem -passin pass:ohpe3yoo3Oap5dohsahya1eeBieweehohseitaet
```

# files
certs generated will go to /data/newcerts
pkcs12 generated will go to /data/issued
pkcs12 revoked will go to /data/revoked


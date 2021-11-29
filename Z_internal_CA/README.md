# Description

The files in this directory are used to secure internal network traffic between containers with SSL.


# commands

CA password: heeme8ahGh5ki1iecu4e

generating CA key
```
openssl genrsa -des3 -out myCA.key 2048
```

generate CA cert
```
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem
```

generate and sign new cert for service
```
./createCert.sh 10.0.0.20
```

push certs to containers
```
./deploy.sh
```

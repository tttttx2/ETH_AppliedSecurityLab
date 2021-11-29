# ETH_AppliedSecurityLab

start everything using 

```bash
sudo docker-compose up --build
```

# Access
Access the web interface on [https://client.imovies.ch](https://client.imovies.ch)  
Access to the logging server is on [https://admin:uoVei2phooZ3ateevahf@logs.imovies.ch](https://admin:uoVei2phooZ3ateevahf@logs.imovies.ch)

(at least if networking on your device works as intended, need to be able to ping 10.0.0.5))


# letsencrypt certificate
sudo certbot certonly --manual --preferred-challenges=dns -d *.imovies.ch


# VMs
## 00 - proxy
reverse_proxy
## 01 - core
core
## 02 - web
web
## 03 - mysql
mysql
## 04 - log
logging_view
logging_store
logging_rsyslog
## 05 - backup
backup

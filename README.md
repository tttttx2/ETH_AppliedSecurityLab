# ETH_AppliedSecurityLab
## Build from source
For development purposes you can build everything from source using

```bash
git clone git@github.com:tttttx2/ETH_AppliedSecurityLab.git
cd ETH_AppliedSecurityLab
sudo docker-compose up --build  
```
## Use distributed VMs
For production purposes setup the VMs provided during the group exchange. They're basically just ubuntu server VMs with networking setup as compatible as possible to the docker-compose configuration.
Make sure to start in the following order: 00, 05, 04, 03, 01, 02

# Access
A simple landing page is located on [https://imovies.ch/](https://imovies.ch/)

Access the client web interface on [https://client.imovies.ch](https://client.imovies.ch)  
Access to the logging server is on [https://logs.imovies.ch](https://logs.imovies.ch)  
Access to the admin web interface is on [https://client.imovies.ch/admin](https://client.imovies.ch/admin)  

Admin credentials are: `admin:uoVei2phooZ3ateevahf`  
SSH access is done using VM 00 as a jumphost. Credentials are the same as above.

User credentials are defined in the project description


If networking on your setup works as intended, you should be able to ping 10.0.0.5  
*.imovies.ch resolves to 10.0.0.5

# Containers distributed on VMs
The process of setting up VMs is not fully automated, however files in `Z_VM_installer` are helpful.
## 00 - proxy
reverse_proxy
## 01 - core
core
## 02 - web
web
## 03 - mysql
mysql  
mysql_store
## 04 - log
logging_view  
logging_store  
logging_rsyslog
## 05 - backup
backup



# Further Notes
## letsencrypt certificate
the cert used on reverse_proxy was generated using

```bash
sudo certbot certonly --manual --preferred-challenges=dns -d *.imovies.ch
```
## internal CA
For internal networking purposes, https traffic uses the internal CA found in `Z_internal_CA`

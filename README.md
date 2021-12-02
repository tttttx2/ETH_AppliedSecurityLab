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
Make sure to start in the following order: 05, 04, 03, 01, 02, 00

# Access
If networking on your setup works as intended, you should be able to ping 10.0.1.5. Otherwise please try adding a static route `sudo ip route add 10.0.1.5 dev vboxnet1` and make sure vboxnet1 is configured properly.
*.imovies.ch resolves to 10.0.1.5

In case this does not work as expected, feel free to overwrite this in the hosts file of your host machine to update those addresses to the one issued on the host-only adapter of `VM 00`

A simple landing page is located on [https://imovies.ch/](https://imovies.ch/) (and yes, we seriously just bought the domain for your convenience)

Access the client web interface on [https://client.imovies.ch](https://client.imovies.ch)  
Access to the logging server is on [https://logs.imovies.ch](https://logs.imovies.ch)  
Access to the admin web interface is on [https://client.imovies.ch/admin](https://client.imovies.ch/admin)  

Admin credentials are: `admin:uoVei2phooZ3ateevahf`  
Test credentials are: `test:testtest`  

Predefined user credentials are defined in the project description
Each exported certificate is protected with the password `imovies`.

SSH access is done using VM 00 as a jumphost. SSH certificate for the user `administrator` (with key password `uoVei2phooZ3ateevahf`) (or password which is the same as above) is located in the folder `Z_VM_installer` or as seen below.

root SSH privkey
```
-----BEGIN OPENSSH PRIVATE KEY-----
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
3tQY9qe3vuQK2vG54u++3nHAfCY=
-----END OPENSSH PRIVATE KEY-----
```

root SSH pubkey
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC+2I99g1sHn4mQZQHeamgr1enBvnnvPiJv+TPLgcwSlOxCgmkfATj/rLBwtqJ0pbasklSBOq83cYlwCIzv24LR94SUKAwOF3n4C6wAZHlD4+Q14+todT9xMf9fNTmhvmHgBmqGNANYtTKWoNyKUN3Xk9Vh8V6As6KsZ+nrgQzwPWlIBWsjf6azLue/0hT7QesRtCKW308GEvOW2nwcqJOZowoN/+NDeTuKXIWgITvluaAIwKl2sH6m/TZgB1s3617g1LLAWH/wIjtriVxn04kNyVKSVFtYLj6xA0myMWNSciLntJx8Ym62dG0l1z8fNzX3hJWYc86TFT4d8uLAc/ImKBDOGSbXliSm8LbAzw2Gg9BytT0EGxSgRmaFGpYv5x7ilirog9RKuU2MbvytboN08MfubvFUOYxcSlUxWCyd7nEBJfqMOtCVXttbVns2GFfmHk+VYxX09ozXIE+FolyuScoApvASVDJH+le2ROM/MAWed+oI1yC+3svOvLkFVrc= root@imovies.ch
```

# Containers distributed on VMs
The process of setting up VMs is not fully automated, however files in `Z_VM_installer` are helpful. Network adapters are as defined below, the ones disconnected are only used during development. Bridged networks allow internet access (if the static IP of the VM is compatible with your network setup. Currently 192.168.1.240-245 are assigned statically. Check/modify the netplan config in /etc/netplan/). The config for host-only should be: no DHCP, IP is 10.0.1.100/24. Maybe needs a static route to 10.0.1.5 on your host machine.
## 00 - proxy
### containers
reverse_proxy
### Network adapter
NET_ADAPTER_0: internal, imovies  
NET_ADAPTER_1: host-only, connected  
NET_ADAPTER_2: bridged, not connected
## 01 - core
### containers
core
### Network adapter
NET_ADAPTER_0: internal, imovies  
NET_ADAPTER_1: host-only, not connected  
NET_ADAPTER_2: bridged, not connected
## 02 - web
### containers
web
### Network adapter
NET_ADAPTER_0: internal, imovies  
NET_ADAPTER_1: host-only, not connected  
NET_ADAPTER_2: bridged, not connected
## 03 - mysql
### containers
mysql  
mysql_store
### Network adapter
NET_ADAPTER_0: internal, imovies  
NET_ADAPTER_1: host-only, not connected  
NET_ADAPTER_2: bridged, not connected
## 04 - log
### containers
logging_view  
logging_store  
logging_rsyslog
### Network adapter
NET_ADAPTER_0: internal, imovies  
NET_ADAPTER_1: host-only, not connected  
NET_ADAPTER_2: bridged, not connected
## 05 - backup
### containers
backup
### Network adapter
NET_ADAPTER_0: internal, imovies  
NET_ADAPTER_1: host-only, not connected  
NET_ADAPTER_2: bridged, not connected


# Further Notes

![network_as_lab_overview](https://github.com/tttttx2/ETH_AppliedSecurityLab/blob/main/network_as_lab_overview.png)

## letsencrypt certificate
the cert used on reverse_proxy was generated using
```bash
sudo certbot certonly --manual --preferred-challenges=dns -d *.imovies.ch
```
## internal CA
For internal networking purposes, https traffic uses the internal CA found in `Z_internal_CA`

## reset DB
In case you want to reset the DB to it's initial state, delete all contents in /root/mysql/data/ on VM03

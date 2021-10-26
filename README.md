# ETH_AppliedSecurityLab

start everything using 

```bash
sudo docker-compose up --build
```

# Access
Access on imovies.ch, if networking on your device works as intended (need to be able to ping 10.0.0.5)


# letsencrypt certificate
sudo certbot certonly --manual --preferred-challenges=dns -d *.imovies.ch


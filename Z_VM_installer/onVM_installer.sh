#!/bin/bash 
## RUN THIS AS ROOT!

# install docker and remote ssh access
apt install -y docker ssh-server

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCs9MpkMkt0UeVrl4jPRs4lNYHgYU95l9aEYpJybClCEFDIn5ahsW96WLLdbe5cfdJhlNzxDvqbrJmPr5tmwYpp3byseJzUwYkwUigl9naLEQjXgOoTeQEIJF1HXHuInvRTr21i7HlS6GfaNWDyumasW1SOvECg2K/yV+mZbucMmt88s0jpQAON/65G8m3mlLSQeMQkfahNr1/rXbKAWDvjwBAhg/xoukhsAwlmjvE2MNBCnkv0KPASBD/Q/A/Wdc1NdG6mUJZoTLjq1UfkEj/ncMHOsQm52rha7/xZBuyxeTfgnt1z5C7LPN8Nhl1sMwwFNkr8TO+DWp6iV3+ihgYp toni@comp370" > /root/.ssh/authorized_keys

# setup src files
mv 0*/* /root/
mv 0*/.* /root/
cp netplan.yaml /etc/netplan/99_config.yaml

# setup host networking
netplan apply

# setup services
echo -e "[Unit]\nDescription=docker-compose-up\n\n[Service]\nExecStart=/root/onVM_run.sh &\n\n[Install]\nWantedBy=multi-user.target" > /lib/systemd/system/imovies.service

systemctl enable docker.service
systemctl enable containerd.service
systemctl enable imovies.service



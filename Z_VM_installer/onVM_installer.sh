#!/bin/bash 
## RUN THIS AS ROOT!


echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCs9MpkMkt0UeVrl4jPRs4lNYHgYU95l9aEYpJybClCEFDIn5ahsW96WLLdbe5cfdJhlNzxDvqbrJmPr5tmwYpp3byseJzUwYkwUigl9naLEQjXgOoTeQEIJF1HXHuInvRTr21i7HlS6GfaNWDyumasW1SOvECg2K/yV+mZbucMmt88s0jpQAON/65G8m3mlLSQeMQkfahNr1/rXbKAWDvjwBAhg/xoukhsAwlmjvE2MNBCnkv0KPASBD/Q/A/Wdc1NdG6mUJZoTLjq1UfkEj/ncMHOsQm52rha7/xZBuyxeTfgnt1z5C7LPN8Nhl1sMwwFNkr8TO+DWp6iV3+ihgYp toni@comp370" > /root/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC+2I99g1sHn4mQZQHeamgr1enBvnnvPiJv+TPLgcwSlOxCgmkfATj/rLBwtqJ0pbasklSBOq83cYlwCIzv24LR94SUKAwOF3n4C6wAZHlD4+Q14+todT9xMf9fNTmhvmHgBmqGNANYtTKWoNyKUN3Xk9Vh8V6As6KsZ+nrgQzwPWlIBWsjf6azLue/0hT7QesRtCKW308GEvOW2nwcqJOZowoN/+NDeTuKXIWgITvluaAIwKl2sH6m/TZgB1s3617g1LLAWH/wIjtriVxn04kNyVKSVFtYLj6xA0myMWNSciLntJx8Ym62dG0l1z8fNzX3hJWYc86TFT4d8uLAc/ImKBDOGSbXliSm8LbAzw2Gg9BytT0EGxSgRmaFGpYv5x7ilirog9RKuU2MbvytboN08MfubvFUOYxcSlUxWCyd7nEBJfqMOtCVXttbVns2GFfmHk+VYxX09ozXIE+FolyuScoApvASVDJH+le2ROM/MAWed+oI1yC+3svOvLkFVrc= root@imovies.ch" >> /root/.ssh/authorized_keys


# setup src files
rm deploy.sh
mv * /root/
mv .* /root/

# setup services
echo -e "[Unit]\nDescription=docker-compose-up\n\n[Service]\nExecStart=/root/onVM_run.sh &\n\n[Install]\nWantedBy=multi-user.target" > /lib/systemd/system/imovies.service

systemctl enable docker.service
systemctl enable containerd.service
systemctl enable imovies.service



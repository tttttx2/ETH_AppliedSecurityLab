#!/bin/bash
echo "0 * * * * /usr/bin/curl -kX GET https://localhost/backup" | crontab -
service cron start


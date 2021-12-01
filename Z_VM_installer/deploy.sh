#!/bin/bash

case "$1" in
  "00")
    scp -r 00 administrator@192.168.1.240:/home/administrator/
    ;;
  "01")
    scp -r 01 administrator@192.168.1.241:/home/administrator/
    ;;
  "02")
    scp -r 02 administrator@192.168.1.242:/home/administrator/
    ;;
  "03")
    scp -r 03 administrator@192.168.1.243:/home/administrator/
    ;;
  "04")
    scp -r 04 administrator@192.168.1.244:/home/administrator/
    ;;
  "05")
    scp -r 05 administrator@192.168.1.245:/home/administrator/
    ;;
  *)
    echo "You have failed to specify what to do correctly."
    exit 1
    ;;
esac


#scp -r 00 administrator@192.168.1.241:/home/administrator/
#scp -r 01 administrator@192.168.1.242:/home/administrator/

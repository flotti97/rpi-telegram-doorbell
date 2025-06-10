#!/bin/bash

source "$(dirname "$0")/.env"

sudo mkdir -p /mnt/samba
sudo mount -t cifs "//$SAMBA_HOST/images" /mnt/samba \
  -o username=$SAMBA_USER,password=$SAMBA_PASS,port=$SAMBA_PORT,vers=3.0,uid=1000,gid=1000,file_mode=0777,dir_mode=0777,nounix,noserverino

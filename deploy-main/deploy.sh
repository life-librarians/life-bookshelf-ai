#!/bin/bash

mkdir -p /home/ec2-user/deploy/zip
cd /home/ec2-user/deploy/zip/

docker-compose down

aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 211125363878.dkr.ecr.ap-northeast-2.amazonaws.com

docker-compose pull

docker-compose up -d

#!/bin/bash
docker stop paraguas
docker rm paraguas
docker rmi el-paraguas-bot:latest
docker build -t el-paraguas-bot .
docker run -it -d --name paraguas el-paraguas-bot

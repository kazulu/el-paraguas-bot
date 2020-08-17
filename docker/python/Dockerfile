FROM python:3.8

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /usr/src/app

COPY ./app .

RUN curl https://raw.githubusercontent.com/kazulu/el-paraguas-bot/master/requirements.txt -o requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

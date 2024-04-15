FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN python setup.py

# Installiere Cron
RUN apt-get update && apt-get -y install cron

COPY run_script.sh /usr/src/app/run_script.sh
RUN chmod +x /usr/src/app/run_script.sh

RUN (crontab -l ; echo "*/2 * * * * /usr/src/app/run_script.sh >> /var/log/cron.log 2>&1") | crontab -


CMD ["cron", "-f"]

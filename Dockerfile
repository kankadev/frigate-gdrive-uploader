FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN python setup.py

# Installiere Cron
RUN apt-get update && apt-get -y install cron

# Füge das Cron-Skript hinzu
COPY run_script.sh /etc/periodic/2min/run_script.sh

# Erstelle den Cronjob
RUN (crontab -l ; echo "*/2 * * * * /etc/periodic/2min/run_script.sh") | crontab -

# Führe den Cron-Daemon aus
CMD ["cron", "-f"]

# frigate-gdrive-uploader
Transfers all Frigate clips that have not yet been uploaded to Google Drive.            


# Requirements
- python 3.8


# Installation
1. clone this repository
2. rename `env_example` to `.env` and change values to your needs
3. run `python setup.py` in project root directory to install all required packages
4. create a project in google cloud console and enable drive api
5. download the credentials json file from Google and copy its content to `credentials/google_drive_credentials.json`
6. run `python main.py` in project root directory, e.g. as a cronjob every minute to check for new clips and upload them every minute


# Known opportunities for improvement
- "real time" upload of clips instead of cronjob, check MQTT documentation for Frigate
- log rotation
- clean up SQLite database automatically frequently
- push notifications in case of errors (e.g. telegram bot, Discord, Mattermost, Gotify, etc.)
- dockerize this project
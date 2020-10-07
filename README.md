# getmydocsbot

Bot to get files from a given path on a computer/VM through Telegram or Discord.

## Installation:
```
  git clone https://github.com/retiolus/getmydocsbot.git
  cd getmydocsbot
  sh install.sh
  crontab -e
```
In the cron config, add the following lines:
```
  @reboot /<path/to>/getmydocsbot/telegram_bot.py
  @reboot /<path/to>/getmydocsbot/discord_bot.py
```

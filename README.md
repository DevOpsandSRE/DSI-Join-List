# DSI-Join-List
This is a Discord bot to query member IDs by join time. The bot will output a list of user IDs if a user's server join time falls within the range provided by the user. This is essential if you need to ban members in bulk if a server raid were to arise. 

## Deploying
This bot will be using Docker and docker compose. Please ensure you have both installed. 

* Make a copy of `config.json.example` and name it `config.json`. Replace the contents to the necessary values (token, staff role name, etc). Yes, you will need to create a token as you would with any other Discord bot.
* The default password for the database is `password`. For security purposes, change this to another password. Change this in both `config.json` and `docker-compose.yml`.
* Run `docker-compose up -d`
* All set!

## Commands
Below are the commands needed to use the bot.

**fetch** is the only command for this particular bot. Assuming the prefix is left as `--`, the command would be `--fetch` followed by the date range:
```
--fetch 2021-06-18 08:16:00; 2021-06-19 00:31:00
```
**Take note that the time used by the bot is UTC time, so the time given to the bot must be in UTC, not the time on the Discord server.**

The response from the bot will be something like:
```
Join Bot: 94385093845093845
43598304958309485
43049850938450396
38293939393939392
82379487239847923
```

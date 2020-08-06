# python-starter-bot
Starter bot to compete in Praetor Poker matches

## Third-party Dependencies:
  - treys
  - websockets
  
## To Use:
Download/clone this repo and update the variables on lines 22-24 in ```bot.py``` (```my_player_id```, ```my_public_username```, ```my_secret_string```) to the values corresponding to your praetorpoker.com account. 

Once you are ready to communicate with the webserver, run the bot with the command

```python bot.py <match_id>```, where ```match_id``` is the match ID for your match. The bot's first action will be to check in with the game server. The match will begin when both players are checked in.

### Logging
This bot logs all communication to and from the game server into a file called ```game_log.log```. The log file's default location is the top level of the repo.
  
### Note
This bot is not good at poker! It's primary purpose is to give participants a quick start with the Praetor Poker communication protocol. 

To that end, feel free to report bugs / mistakes / refactors that would improve the bot. 

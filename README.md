# libot-lb
*Based on [lightningbolts/Lichess-Bot-Leaderboards](https://github.com/lightningbolts/Lichess-Bot-Leaderboards)*

A leaderboard for all Lichess Bots. It checks for list of online bots using [Lichess' Bot API](https://lichess.org/api#tag/Bot/operation/apiBotOnline) and creates a list ([available_bots.txt](./available_bots.txt)). Everytime it runs this list is checked to see if any online bots aren't in it and if they aren't, those bots are added to the list. Once that's done, using Lichess' API, the [bots public data](https://lichess.org/api#tag/Users/operation/apiUser) is taken to get the bots rating (This might take a while!). This data is converted into `json` format and is then easily sorted based on rating in each game type (or variant).

## Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Execute python script:
```bash
python3 bot_leaderboard.py
```
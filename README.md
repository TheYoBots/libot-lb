# libot-lb
*Based on [lightningbolts/Lichess-Bot-Leaderboards](https://github.com/lightningbolts/Lichess-Bot-Leaderboards)*

A leaderboard for all Lichess Bots. It checks for list of online bots using [Lichess' Bot API](https://lichess.org/api#tag/Bot/operation/apiBotOnline) and creates a list ([available_bots.txt](./available_bots.txt)). Everytime it runs this list is checked to see if any online bots aren't in it and if they aren't, those bots are added to the list. Once that's done, using Lichess' API, the [bots public data](https://lichess.org/api#tag/Users/operation/apiUsers) is taken to get the bots rating. This data is converted into `json` format and then each of the [rules](#rules) are checked (This will take a while!) and is then sorted based on rating in each game type (or variant).

## Run
1. Set Environment Secret:

Get a [Token from lichess (No scopes required)](https://lichess.org/account/oauth/token/create?scopes[]=None&description=Bot+Leaderboard+Token) and execute the following command:
```
# windows
set TOKEN='your-token-here'

# linux
export TOKEN='your-token-here'
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Execute python script:
```bash
python3 bot_leaderboard.py
```

## Rules
#### [Bot Leaderboard](./bot_leaderboard/)
1. Your Bot must not be named in the [Banned Bots List](https://lichess.org/team/banned-of-leaderboard-of-bots) for any of the following reasons:
   - For "farming" weaker opponents/Bots.
   - For playing only against human opponents with your Bot.
   - For playing too often against other Bots that you own/operate (or "siblings").
   - Or any other reason for which your Bot is listed in [this Lichess Team](https://lichess.org/team/banned-of-leaderboard-of-bots).
2. Your Bot must have played at least 1 rated game in the week in that respective Variant/Game type.
3. Your Bot must not have Provisional Rating (with a ?) in that respective Variant/Game type.
4. Your Bot must not have a mark that indicates violation of [Lichess' Terms of Service](https://lichess.org/terms-of-service).
5. Your Bot must have played at least 50 rated games in that respective Variant/Game type.
6. Your Bot must have a rating deviation lower than 75, in Standard Chess, and lower than 65 in Variants.
#### [Unrestricted Bot Leaderboard](./unrestricted_bot_leaderboard/)
1. Your Bot must have played at least 50 rated games in that respective Variant/Game type.
2. Your Bot must not have a mark that indicates violation of [Lichess' Terms of Service](https://lichess.org/terms-of-service).
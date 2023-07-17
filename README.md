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

## Rules
1. Your Bot must not me named in the [Banned Bots List](https://lichess.org/team/banned-of-leaderboard-of-bots) for any of the following reasons:
   - For "farming" weaker opponents/Bots.
   - For playing only against human opponents with your Bot.
   - For playing too often against your other Bots that you own/operate (or "siblings").
   - Or any other reason for which your named is listed in [this Lichess Team](https://lichess.org/team/banned-of-leaderboard-of-bots).
2. Your Bot must have played at least 1 rated game in the week in that respective Variant/Game type.
3. Your Bot must not have Provisional Rating (with a ?) in that respective Variant/Game type.
4. Your Bot must not have a mark that indicates violation of [Lichess' Terms of Service](https://lichess.org/terms-of-service).
5. Your Bot must have played at least 50 rated games in that respective Variant/Game type.
6. Your Bot must have a Rating Deviation (rd) that is strictly less than 65 in that respective Variant/Game type.

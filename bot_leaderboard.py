import urllib.request
import orjson
import sys
import lichess.api
from lichess.format import SINGLE_PGN
import json
import os
import datetime
import re

TOKEN = os.environ['TOKEN']

def types():
    return [
        'bullet', 'blitz',  'rapid', 'classical', 'correspondence', 'chess960',
        'antichess', 'atomic', 'crazyhouse', 'horde', 'kingOfTheHill', 'racingKings', 'threeCheck'
    ]

def get_file_name(type):
    return './bot_leaderboard/' + type + '.md'

def get_banned_bots():
    return [
        'caissa-ai', 'ProteusSF', 'ProteusSF-lite', 'ProteusSF-Open', 'ProteusSF-Turbo', 'QalatBotEngine', 'Vaxim2000', 'Viet-AI', 'RexherBot', 'YellowFlash_v2',  'GHDES', 'Anand_Bot', 'SamuraiX_v1', 'WhatsANikitosikHUH', 'OkayWhyYouReadinThis',
        'MedipolUniversity', 'MustafaYilmazBot', 'CodingAdventureBot',
        'Nikitosikbot', 'Nikitosik-ai', 'caissa-test'
    ]

def get_user_last_rated(username, type):
    now = datetime.datetime.utcnow()
    since = now - datetime.timedelta(days=7)
    since = int(since.timestamp() * 1000)
    user = lichess.api.user_games(username, max=1, rated='true', perfType=type, since=since, format=SINGLE_PGN, auth=TOKEN)
    match = re.search(r'\[UTCDate "(.*?)"\]', user)
    if match:
        return match.group(1)
    else:
        print(f"BOT {username}: No rated games for 1 week")
        return "2000.01.01"  # random default date

def get_available_bots():
    available_bots = set()
    try:
        with open('available_bots.txt', 'r') as f:
            available_bots = []
            for bot in f.readlines():
                available_bots.append(bot.strip())
            available_bots = sorted(available_bots)
        with urllib.request.urlopen('https://lichess.org/api/bot/online') as online_bots:
            for i in online_bots:
                d = orjson.loads(i)
                if d['id'] not in available_bots:
                    available_bots.append(d['id'])
                    print(f"Adding {d['id']} to available bots list")
    except Exception as e:
        print(e)
    with open('available_bots.txt', 'w') as f:
        for bot in available_bots:
            f.write(bot + '\n')
    print(f"Updated List of Bots")

def get_all_bot_ratings():
    all_bot_ratings = []
    with open('available_bots.txt', 'r') as f:
        available_bots = [bot.strip() for bot in f.readlines()]

    batch_size = 100
    num_batches = (len(available_bots) + batch_size - 1) // batch_size

    for i in range(num_batches):
        batch_start = i * batch_size
        batch_end = (i + 1) * batch_size
        batch_usernames = available_bots[batch_start:batch_end]

        users_list = lichess.api.users_by_ids(batch_usernames)

        for user in users_list:
            all_bot_ratings.append({
                'username': user.get('username'),
                'perfs': user.get('perfs', {}),
                'seenAt': user.get('seenAt'),
                'tosViolation': user.get('tosViolation'),
                'disabled': user.get('disabled')
            })

    with open('bot_leaderboard.json', 'w') as f:
        json.dump(all_bot_ratings, f)
    print("Updated bot_leaderboard.json file.")

def get_bot_leaderboard(type):
    banned_bots = get_banned_bots()

    file_path = os.path.join(os.path.dirname(__file__), 'bot_leaderboard.json')
    with open(file_path, 'r') as f:
        bot_ratings = json.load(f)

    user_arr = []
    count = 1

    for d in bot_ratings:
        perfs = d['perfs'].get(type)
        if perfs is not None:
            result = [d['username'], perfs.get('rating')]
            print(f'BOT {result[0]}: {result[1]} in {type}.')
            now = datetime.datetime.utcnow()
            d['seenAt'] = datetime.datetime.utcfromtimestamp(d['seenAt'] / 1000)
            if perfs.get('prov', False) == True:
                print("Provisional rating")
            elif d.get('tosViolation', False) == True:
                print("Violated ToS")
            elif perfs.get('games', 0) <= 50:
                print("Too few games played")
            elif type in ['bullet', 'blitz', 'rapid', 'classical'] and perfs.get('rd', 0) >= 75:
                print("High rating deviation")
            elif type not in ['bullet', 'blitz', 'rapid', 'classical'] and perfs.get('rd', 0) >= 65:
                print("High rating deviation")
            elif (now - d['seenAt']) > datetime.timedelta(days=7):
                print("Not active for 1 week")
            elif result[0] in banned_bots:
                print("Banned Bot")
            elif d.get('disabled', False) == True:
                print("Account Closed")
            elif get_user_last_rated(result[0], type) != "2000.01.01":
                user_arr.append(result)
            else:
                print(f"BOT {d['username']}: No {type} rating available")
        else:
            print(f"BOT {d['username']}: No {type} rating available")
    resulting_arr = sorted(user_arr, key=lambda x: x[1], reverse=True)
    with open(get_file_name(type), 'w') as f:
        print("Rank|Bot|Rating", file=f)
        print("---|---|---", file=f)
        for j in resulting_arr:
            print(f"#{str(count)}|@{j[0]}|{str(j[1])}", file=f)
            count += 1

    print(f"Finished generating leaderboard for {type}")

if __name__ == "__main__":
    try:
        get_available_bots()
        get_all_bot_ratings()
        for i in types():
            get_bot_leaderboard(i)
    except KeyboardInterrupt:
        sys.exit()

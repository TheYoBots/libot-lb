import urllib.request
import orjson
import sys
import lichess.api

def types():
    return [
        'bullet',
        'blitz',
        'rapid',
        'classical',
        'correspondence',
        'antichess',
        'atomic',
        'chess960',
        'crazyhouse',
        'horde',
        'kingOfTheHill',
        'racingKings',
        'threeCheck'
    ]

def get_file_name(type):
    return './bot_leaderboard/' + type + '.md'

def get_banned_bots():
    return [
        'caissa-ai',
        'ProteusSF',
        'ProteusSF-lite',
        'ProteusSF-Open',
        'ProteusSF-Turbo',
        'QalatBotEngine',
        'Vaxim2000',
        'Viet-AI',
        'MedipolUniversity',
        'MustafaYilmazBot'
    ]

def get_user_rating(username, type):
    user = lichess.api.user(username)
    return [username, user.get('perfs', {}).get(type, {}).get('rating'), user.get('perfs', {}).get(type, {}).get('prov'), user.get('tosViolation')]

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
                if d['username'] not in available_bots:
                    available_bots.append(d['username'])
    except Exception as e:
        print(e)
    with open('available_bots.txt', 'w') as f:
        for bot in available_bots:
            f.write(bot + '\n')
    print(f"Updated List of Bots")

def get_bot_ratings_online(type):
    banned_bots = get_banned_bots()
    with open('available_bots.txt', 'r') as f:
        available_bots = []
        for bot in f.readlines():
            available_bots.append(bot.strip())

    user_arr = []

    for bot in available_bots:
        result = get_user_rating(bot, type)
        if result is not None:
            if result[0] not in banned_bots and result[1] is not None and result[2] != True and result[3] != True:
                user_arr.append(result)
                print(f'BOT {result[0]}: {result[1]} in {type}')

    resulting_arr = sorted(user_arr, key=lambda x: x[1], reverse=True)

    with open(get_file_name(type), 'w') as f:
        count = 1
        print(f"Rank|Bot|Rating", file=f)
        print("---|---|---", file=f)
        for j in resulting_arr:
            print(f"#{str(count)}|@{j[0]}|{str(j[1])}", file=f)
            count += 1

    print(f"Finished generating leaderboard for {type}")

if __name__ == "__main__":
    try:
        get_available_bots()
        for i in types():
            get_bot_ratings_online(i)
    except KeyboardInterrupt:
        sys.exit()
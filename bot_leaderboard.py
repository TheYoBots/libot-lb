import urllib.request
import orjson
import sys
import lichess.api
import json
import os

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
        'RexherBot',
        'MedipolUniversity',
        'MustafaYilmazBot'
    ]

def get_user_rating(username):
    user = lichess.api.user(username)
    return {
        'username': user.get('username'),
        'perfs': user.get('perfs', {}),
        'tosViolation': user.get('tosViolation')
    }

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
                    print(f"Adding {d['username']} to available bots list")
    except Exception as e:
        print(e)
    with open('available_bots.txt', 'w') as f:
        for bot in available_bots:
            f.write(bot + '\n')
    print(f"Updated List of Bots")

def get_bot_ratings_online(type):
    banned_bots = get_banned_bots()

    file_path = os.path.join(os.path.dirname(__file__), 'bot_leaderboard.json')
    with open(file_path, 'r') as f:
        bot_ratings = json.load(f)

    user_arr = []
    count = 1

    for d in bot_ratings:
        try:
            result = [d['username'], d['perfs'][type]['rating']]
            print(f'BOT {result[0]}: {result[1]} in {type}.')
            try: 
                if d['perfs'][type]['prov'] == True:
                    print("Provisional rating")
                if d['tosViolation'] == True:
                    print("Violated ToS")
                if d['perfs'][type]['games'] <= 50:
                    print("Too few games played")
                if d['perfs'][type]['rd'] >= 65:
                    print("High rating deviation")
            except:
                if result[0] not in banned_bots:
                    user_arr.append(result)
        except:
            print(f"BOT {d['username']}: No {type} rating available")
    resulting_arr = sorted(user_arr, key=lambda x: x[1], reverse=True)
    with open(get_file_name(type), 'w') as f:
        print("Rank|Bot|Rating", file=f)
        print("---|---|---", file=f)
        for j in resulting_arr:
            print(f"#{str(count)}|@{j[0]}|{str(j[1])}", file=f)
            count += 1

    print(f"Finished generating leaderboard for {type}")

def get_all_bot_ratings():
    all_bot_ratings = []
    with open('available_bots.txt', 'r') as f:
        available_bots = [bot.strip() for bot in f.readlines()]

    for bot in available_bots:
        result = get_user_rating(bot)
        if result is not None:
            all_bot_ratings.append(result)
            print(f'Getting rating of BOT {result["username"]}')

    with open('bot_leaderboard.json', 'w') as f:
        json.dump(all_bot_ratings, f)
    print("Updated bot_leaderboard.json file.")

if __name__ == "__main__":
    try:
        get_available_bots()
        get_all_bot_ratings()
        for i in types():
            get_bot_ratings_online(i)
    except KeyboardInterrupt:
        sys.exit()
import urllib.request
import orjson
import sys

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
        'MedipolUniversity',
        'MustafaYilmazBot'
        'Viet-AI'
    ]

def get_available_bots():
    available_bots = set()
    try:
        with open('available_bots.txt', 'r') as f:
            available_bots = []
            for bot in f.readlines():
                available_bots.append(bot.strip())
            available_bots = sorted(available_bots)
        online_bots = urllib.request.urlopen('https://lichess.org/api/bot/online')
        for i in online_bots:
            d = orjson.loads(i)
            if d['username'] not in available_bots:
                available_bots.append(d['username'])
    except Exception as e:
        print(e)
    with open('available_bots.txt', 'w') as f:
        for bot in available_bots:
            f.write(bot + '\n')

def get_bot_ratings_online(type):
    banned_bots = get_banned_bots()
    online_bots = urllib.request.urlopen('https://lichess.org/api/bot/online')
    user_arr = []
    num_prov = 0
    num_est = 0
    count = 0
    banned = 0
    count2 = 1
    
    try:
        for i in online_bots:
            d = orjson.loads(i)
            try:
                result = [d['username'], d['perfs'][type]['rating']]
                print(f'BOT {result[0]}: {result[1]} in {type}.')
                try: 
                    if d['perfs'][type]['prov'] == True:
                        print(f'BOT {result[0]}: Provisional rating in {type}')
                        num_prov += 1
                except:
                    num_est += 1
                    if result[0] in banned_bots:
                        banned += 1
                    else:
                        user_arr.append(result)
            except:
                print(f"BOT {d['username']}: No {type} rating available")
            count += 1
        resulting_arr = sorted(user_arr, key=lambda x: x[1], reverse=True)
        with open(get_file_name(type), 'w') as f:
            print("{}|{}|{}".format("Rank", "Bot", "Rating"), file=f)
            print("---|---|---", file=f)
            for j in resulting_arr:
                print("#{}|@{}|{}".format(str(count2), j[0], str(j[1])), file=f)
                count2 += 1
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    try:
        types = types()
        for i in types:
            get_bot_ratings_online(i)
        get_available_bots()
    except KeyboardInterrupt:
        sys.exit()
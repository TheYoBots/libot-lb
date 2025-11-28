import urllib.request
import orjson
import sys
import lichess.api
from lichess.format import SINGLE_PGN
import json
import os
import datetime
import re

TOKEN = os.environ.get('TOKEN')
BATCH_SIZE = 100
TYPES = [
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

# Use frozenset for O(1) membership checks in get_bot_leaderboard
STANDARD_VARIANTS = frozenset({'bullet', 'blitz', 'rapid', 'classical'})


def get_file_name(type, dir):
    return os.path.join(dir, f"{type}.md")


r"""
def get_banned_bots():
    banned_bots = set()

    try:
        with urllib.request.urlopen('https://lichess.org/api/team/banned-of-leaderboard-of-bots') as banned_bots_data:
            data = orjson.loads(banned_bots_data.read())
            description = data.get('description', '')
            banned_usernames = re.findall(r'@([\w-]+)', description)
            banned_bots.update(username.lower() for username in banned_usernames)

    except Exception as e:
        print(f"Error fetching banned bots: {e}")

    return banned_bots
"""

def get_user_last_rated(username, type):
    now = datetime.datetime.now(datetime.UTC)
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
            available_bots = {bot.strip() for bot in f if bot.strip()}
        with urllib.request.urlopen('https://lichess.org/api/bot/online') as online_bots:
            for i in online_bots:
                d = orjson.loads(i)
                bot_id = d['id']
                if bot_id not in available_bots:
                    available_bots.add(bot_id)
                    print(f"Adding {bot_id} to available bots list")
    except Exception as e:
        print(e)
    # Sort only once when writing to file
    sorted_bots = sorted(available_bots)
    with open('available_bots.txt', 'w') as f:
        f.write('\n'.join(sorted_bots) + '\n')
    print("Updated List of Bots")


def get_all_bot_ratings():
    all_bot_ratings = []
    with open('available_bots.txt', 'r') as f:
        available_bots = [bot.strip() for bot in f.readlines()]

    num_batches = (len(available_bots) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(num_batches):
        batch_start = i * BATCH_SIZE
        batch_end = (i + 1) * BATCH_SIZE
        batch_usernames = available_bots[batch_start:batch_end]

        users_list = lichess.api.users_by_ids(batch_usernames)

        for user in users_list:
            all_bot_ratings.append({
                'username': user.get('username'),
                'id': user.get('id'),
                'perfs': user.get('perfs', {}),
                'seenAt': user.get('seenAt'),
                'tosViolation': user.get('tosViolation'),
                'disabled': user.get('disabled')
            })

    with open('bot_leaderboard.json', 'w') as f:
        json.dump(all_bot_ratings, f)
    print("Updated bot_leaderboard.json file.")


def get_bot_leaderboard(type, unrestricted=False, bot_ratings=None):
#   banned_bots = get_banned_bots()

    # Reuse bot_ratings if passed to avoid redundant file reads
    if bot_ratings is None:
        file_path = os.path.join(os.path.dirname(__file__), 'bot_leaderboard.json')
        with open(file_path, 'r') as f:
            bot_ratings = json.load(f)

    user_arr = []
    count = 1
    now = datetime.datetime.now(datetime.UTC)
    one_week = datetime.timedelta(days=7)
    is_standard_variant = type in STANDARD_VARIANTS

    for d in bot_ratings:
        perfs = d['perfs'].get(type)
        if perfs is not None:
            result = [d['username'], perfs.get('rating')]
            print(f'BOT {result[0]}: {result[1]} in {type}.')
            seen_at = datetime.datetime.fromtimestamp(d['seenAt'] / 1000, datetime.UTC)
            if d.get('disabled', False) is True:
                print("Account Closed")
            elif d.get('tosViolation', False) is True:
                print("Violated ToS")
            else:
                if unrestricted:
                    if perfs.get('games', 0) > 0:
                        user_arr.append(result)
                    else:
                        print(f"BOT {d['username']}: No {type} rating available")
                else:
                    if perfs.get('prov', False) is True:
                        print("Provisional rating")
                    elif d.get('tosViolation', False) is True:
                        print("Violated ToS")
                    elif perfs.get('games', 0) <= 50:
                        print("Too few games played")
                    elif is_standard_variant and perfs.get('rd', 0) >= 75:
                        print("High rating deviation")
                    elif not is_standard_variant and perfs.get('rd', 0) >= 65:
                        print("High rating deviation")
                    elif (now - seen_at) > one_week:
                        print("Not active for 1 week")
#                   elif d['id'] in banned_bots:
#                       print("Banned Bot")
                    elif d.get('disabled', False) is True:
                        print("Account Closed")
                    elif get_user_last_rated(result[0], type) != "2000.01.01":
                        user_arr.append(result)
                    else:
                        print(f"BOT {d['username']}: Not qualified for {type} leaderboard")
        else:
            print(f"BOT {d['username']}: No {type} rating available")

    if unrestricted:
        dir = './unrestricted_bot_leaderboard/'
    else:
        dir = './bot_leaderboard/'

    resulting_arr = sorted(user_arr, key=lambda x: x[1], reverse=True)
    with open(get_file_name(type, dir), 'w') as f:
        print("Rank|Bot|Rating", file=f)
        print("---|---|---", file=f)
        for j in resulting_arr:
            print(f"#{str(count)}|@{j[0]}|{str(j[1])}", file=f)
            count += 1

    print(f"Finished generating leaderboard for {type}")


def main():
    try:
        get_available_bots()
        get_all_bot_ratings()
        
        # Load bot ratings once and reuse for all leaderboard generation
        file_path = os.path.join(os.path.dirname(__file__), 'bot_leaderboard.json')
        with open(file_path, 'r') as f:
            bot_ratings = json.load(f)
        
        for i in TYPES:
            get_bot_leaderboard(i, unrestricted=True, bot_ratings=bot_ratings)
            get_bot_leaderboard(i, bot_ratings=bot_ratings)
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()

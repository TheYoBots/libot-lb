from flask import Flask, send_file
import os

app = Flask(__name__)

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

@app.route('/')
@app.route('/home')
def welcome_page():
    return send_file('html/Home.html')

@app.route('/bot')
def bot():
    return send_file('html/Bot.html')

@app.route('/unrestricted')
def unrestricted():
    return send_file('html/Unrestricted.html')

@app.route('/bot-rank')
def botsearch():
    return send_file('html/BotRank.html')

@app.route('/available_bots.txt')
def available_bots_file():
    return send_file('available_bots.txt')

@app.route('/bot_leaderboard/<path:filename>')
def serve_bot_leaderboard_md(filename):
    safe_path = os.path.join(os.path.dirname(__file__), 'bot_leaderboard', filename)
    if os.path.exists(safe_path):
        return send_file(safe_path)
    else:
        return "Not found", 404

@app.route('/js/<path:filename>')
def serve_js(filename):
    safe_path = os.path.join(os.path.dirname(__file__), 'js', filename)
    if os.path.exists(safe_path):
        return send_file(safe_path)
    else:
        return "Not found", 404

@app.route('/bot/<type_name>')
def bot_type(type_name):
    if type_name in TYPES:
        return send_file(f'bot_leaderboard/{type_name}.html')
    else:
        return "Invalid type", 404

@app.route('/unrestricted/<type_name>')
def unrestricted_type(type_name):
    if type_name in TYPES:
        return send_file(f'unrestricted_bot_leaderboard/{type_name}.html')
    else:
        return "Invalid type", 404

if __name__ == "__main__":
    app.run(host="localhost", port=5000)

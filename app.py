from flask import Flask, render_template, jsonify, request
from blackjack import BlackJackGame
from pprint import pprint

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
print(app.config)

game = BlackJackGame()


@app.route('/')
def main():
    return render_template('about.html')


@app.route('/blackjack')
def blackjack():
    return render_template('blackjack.html')


@app.route('/blackjack/start', methods=['POST'])
def start_game():
    global game
    game = BlackJackGame()
    game.start()
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/hit', methods=['POST'])
def hit():
    hand_index = request.form.get('hand_index')
    if hand_index is None:
        hand_index = 0
    else:
        hand_index = int(hand_index)
    game.hit(hand_index)
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/stand', methods=['POST'])
def stand():
    hand_index = request.form.get('hand_index')
    if hand_index is None:
        hand_index = 0
    else:
        hand_index = int(hand_index)
    game.stand(hand_index)
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/double', methods=['POST'])
def double():
    game.double()
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/split', methods=['POST'])
def split():
    game.split()
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


if __name__ == '__main__':
    app.run()

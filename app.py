from flask import Flask, render_template, jsonify, request
from blackjack import BlackJackGame
from pprint import pprint
from slots import spin_slots, check_win
from raketka import RocketGame

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
print(app.config)

game = BlackJackGame()
rocket_game = RocketGame()

@app.route('/')
def main():
    return render_template('about.html')


@app.route('/raketka')
def raketka():
    return render_template('raketka.html')

@app.route('/raketka/play', methods=['POST'])
def play_raketka():
    data = request.get_json()
    bet = int(data.get('bet'))
    auto_stop = float(data.get('auto_stop'))
    result = rocket_game.place_bet(bet, auto_stop)
    return jsonify(result)



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

@app.route('/slots/spin', methods=['POST'])
def spin():
    slots = spin_slots()
    win, message = check_win(slots)
    ret = {
        'slots': slots,
        'message': message,
        'win': win
    }
    pprint(ret)
    return jsonify(ret)

@app.route('/slots')
def slots():
    return render_template('slots.html')


if __name__ == '__main__':
    app.run()

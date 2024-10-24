import json

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session, g

from forms.forms import RegistrationForm, LoginForm
from models.models import User, db
from static.py.blackjack import BlackJackGame
from pprint import pprint
from static.py.slots import spin_slots, check_win
from static.py.raketka import RocketGame

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
db.init_app(app)
print(app.config)

# app = Flask(__name__,)

rocket_game = RocketGame()

def get_game():
    game_data = session.get('blackjack_game')
    if game_data:
        return BlackJackGame.from_dict(json.loads(game_data))
    return BlackJackGame()

def save_game(game):
    session['blackjack_game'] = json.dumps(game.to_dict())


def get_user_balance(user_id):
    user = User.query.get(user_id)
    if user:
        return user.balance
    return 0


@app.before_request
def load_user_balance():
    user_id = session.get('user_id')
    g.balance = 0
    if user_id:
        g.balance = get_user_balance(user_id)

@app.context_processor
def inject_balance():
    return dict(balance=g.balance)


@app.route('/check_balance', methods=['GET'])
def check_balance():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'balance': user.balance})


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
    user_id = session.get('user_id')
    if not user_id:
        flash('User not logged in', 'danger')
        return redirect(url_for('blackjack'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('blackjack'))

    bet = int(request.form.get('bet', 0))
    if user.balance < bet:
        flash('Insufficient balance', 'danger')
        return redirect(url_for('blackjack'))

    user.balance -= bet
    db.session.commit()

    decks_count = int(request.form.get('decks_count', 8))
    game = BlackJackGame()
    game.start(decks_count, bet)
    save_game(game)
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/end', methods=['POST'])
def end_game():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    win = request.form.get('win', type=int)
    print(win)
    user.balance += win
    db.session.commit()

    return jsonify({'success': True, 'new_balance': user.balance})


@app.route('/blackjack/hit', methods=['POST'])
def hit():
    game = get_game()
    hand_index = request.form.get('hand_index')
    if hand_index is None:
        hand_index = 0
    else:
        hand_index = int(hand_index)
    game.hit(hand_index)
    save_game(game)
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/stand', methods=['POST'])
def stand():
    game = get_game()
    hand_index = request.form.get('hand_index')
    if hand_index is None:
        hand_index = 0
    else:
        hand_index = int(hand_index)
    game.stand(hand_index)
    save_game(game)
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/double', methods=['POST'])
def double():
    game = get_game()
    game.double()
    save_game(game)
    ret = game.to_dict()
    pprint(ret)
    return jsonify(ret)


@app.route('/blackjack/split', methods=['POST'])
def split():
    game = get_game()
    game.split()
    save_game(game)
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


# TODO: реализация использования баланса пользователя
@app.route('/lk')
def lk():
    user_id = session.get('user_id')
    if not user_id:
        flash('Войдите, чтобы просматривать эту страницу', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('about'))

    return render_template('lk.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Вход успешный!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Вход в систему не удался. Пожалуйста, проверьте логин и пароль.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('about'))


if __name__ == '__main__':
    app.run()

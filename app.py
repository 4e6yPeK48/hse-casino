from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session

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
    decks_count = int(request.form.get('decks_count', 8))
    game = BlackJackGame()
    game.start(decks_count)
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
        return redirect(url_for('main'))

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
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()

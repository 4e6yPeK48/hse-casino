import random

class RocketGame:
    def __init__(self):
        self.balance = 100 
        self.max_crash_coef = 5.00  
        self.min_bet = 10 
        self.min_auto_stop = 1.25

    def place_bet(self, bet_amount, auto_stop):

        if bet_amount < self.min_bet:
            return "Ставка слишком мала. Минимальная ставка — 10 токенов."
        if auto_stop < self.min_auto_stop:
            return "Автостоп слишком мал. Минимальный автостоп — 1.25."

        if bet_amount > self.balance:
            return "Недостаточно токенов для ставки."


        crash_at = random.triangular(1.25, self.max_crash_coef, 1.5) 
        crash_at = round(crash_at, 2)

        current_coef = 1.00 


        while current_coef < self.max_crash_coef:
            current_coef += 0.01
            current_coef = round(current_coef, 2)


            if current_coef >= auto_stop:
                win_amount = bet_amount * auto_stop
                self.balance += win_amount - bet_amount 
                return {
                    'result': 'win',
                    'message': f"Автостоп сработал! Вы выиграли {win_amount} токенов.",
                    'balance': self.balance,
                    'coef': auto_stop
                }

 
            if current_coef >= crash_at:
                self.balance -= bet_amount
                return {
                    'result': 'lose',
                    'message': f"Ракета сломалась на коэффициенте {crash_at}. Вы потеряли {bet_amount} токенов.",
                    'balance': self.balance,
                    'coef': crash_at
                }

        return "Игра окончена."
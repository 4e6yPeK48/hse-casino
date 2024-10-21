import random


def spin_slots():
    symbols = ['🍒', '🍋', '🍉', '🔔', '⭐', '7'] 
    return [random.choice(symbols) for _ in range(3)] 


def check_win(slots):
    if slots[0] == slots[1] == slots[2]:
        return True, "JAckpot!"
    elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
        return True, "2 ok"
    else:
        return False, "😢"


# def play_slots(rounds=5):
#     print("СЛОТЫ ОТ АСХАБА ТАМАЕВА")
#     for i in range(rounds):
#         print(f"\nРаунд {i + 1}:")
#         slots = spin_slots()
#         print("Ваши символы: ", " | ".join(slots))
#         win, message = check_win(slots)
#         print(message)
#
#     print("гроши переводить сюда")


# play_slots()
$(document).ready(function () {
    const $dealerCards = $('#dealer-cards');
    const $dealerScore = $('#dealer-score');
    const $playerHands = $('#player-hands');
    const $playerScores = $('#player-scores');
    const $result = $('#result');
    const $hit = $('#hit');
    const $hit2 = $('#hit2');
    const $double = $('#double');
    const $split = $('#split');
    const $stand = $('#stand');
    const $stand2 = $('#stand2');
    const $start = $('#start');

    function updateGame(data) {
        if (!data.show_dealer_cards) {
            $dealerCards.html(data.dealer_cards.join(', '));
            $dealerScore.html('<b>Сумма:</b>' + data.dealer_score);
        } else {
            $dealerCards.html(data.dealer_cards[0] + ', *');
            $dealerScore.html('<b>Сумма:</b> *');
        }

        $playerHands.html(data.player_hands.map((hand, index) =>
            `<b>Рука ${index + 1}:</b> ${hand.join(', ')}`).join('<br>'));
        $playerScores.html('<b>Суммы:</b> ' + data.player_scores.join(', '));

        if (data.game_over) {
            $result.html('Результат: ' + data.result.join(', ') + '<br>Был ли дабл: ' + (data.double_check ? 'Да' : 'Нет'));
            $hit.add($hit2).add($double).add($split).add($stand).add($stand2).prop('disabled', true);
        } else {
            $result.html('');
            $hit.add($double).add($split).add($stand).prop('disabled', false);

            if (data.player_hands.length > 1) {
                $hit2.add($stand2).show().prop('disabled', false);
            } else {
                $hit2.add($stand2).hide();
            }

            if (data.first_hand_bust || data.first_hand_stand || data.player_scores[0] >= 21) {
                $hit.prop('disabled', true);
                $stand.prop('disabled', true);
            }

            if (data.second_hand_bust || data.second_hand_stand || (data.player_scores.length > 1 && data.player_scores[1] >= 21)) {
                $hit2.prop('disabled', true);
                $stand2.prop('disabled', true);
            }

            $split.prop('disabled', !data.can_split);
        }
    }

    $start.click(function () {
        $.post('/blackjack/start', function (data) {
            updateGame(data);
            if (!data.game_over) {
                $hit.add($hit2).add($double).add($stand).add($stand2).prop('disabled', false);
                $hit2.add($stand2).hide();
            }
        });
    });

    $hit.click(function () {
        $.post('/blackjack/hit', function (data) {
            updateGame(data);
        });
    });

    $hit2.click(function () {
        $.post('/blackjack/hit', {hand_index: 1}, function (data) {
            updateGame(data);
        });
    });

    $stand.click(function () {
        $.post('/blackjack/stand', function (data) {
            updateGame(data);
            if (data.first_hand_stand) {
                $hit.prop('disabled', true);
                $stand.prop('disabled', true);
            }
        });
    });

    $stand2.click(function () {
        $.post('/blackjack/stand', {hand_index: 1}, function (data) {
            updateGame(data);
            if (data.second_hand_stand) {
                $hit2.prop('disabled', true);
                $stand2.prop('disabled', true);
            }
        });
    });

    $double.click(function () {
        $.post('/blackjack/double', function (data) {
            updateGame(data);
        });
    });

    $split.click(function () {
        $.post('/blackjack/split', function (data) {
            updateGame(data);
        });
    });
});

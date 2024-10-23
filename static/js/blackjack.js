$(document).ready(function () {
    const $dealerCards = $('#dealer-cards');
    const $dealerScore = $('#dealer-score');
    const $playerHands = $('#player-hands');
    const $playerCardsContainer = $('#player-cards-container');
    const $dealerCardsContainer = $('#dealer-cards-container');
    const $playerScores = $('#player-scores');
    const $result = $('#result');
    const $hit = $('#hit');
    const $hit2 = $('#hit2');
    const $double = $('#double');
    const $split = $('#split');
    const $stand = $('#stand');
    const $stand2 = $('#stand2');
    const $start = $('#start');

    const cardShortNames = {
        'Туз ♠ пики': 'A♠️',
        '2 ♠ пики': '2♠️',
        '3 ♠ пики': '3♠️',
        '4 ♠ пики': '4♠️',
        '5 ♠ пики': '5♠️',
        '6 ♠ пики': '6♠️',
        '7 ♠ пики': '7♠️',
        '8 ♠ пики': '8♠️',
        '9 ♠ пики': '9♠️',
        '10 ♠ пики': '10♠️',
        'Валет ♠ пики': 'J♠️',
        'Дама ♠ пики': 'Q♠️',
        'Король ♠ пики': 'K♠️',
        'Туз ♥ черви': 'A♥️',
        '2 ♥ черви': '2♥️',
        '3 ♥ черви': '3♥️',
        '4 ♥ черви': '4♥️',
        '5 ♥ черви': '5♥️',
        '6 ♥ черви': '6♥️',
        '7 ♥ черви': '7♥️',
        '8 ♥ черви': '8♥️',
        '9 ♥ черви': '9♥️',
        '10 ♥ черви': '10♥️',
        'Валет ♥ черви': 'J♥️',
        'Дама ♥ черви': 'Q♥️',
        'Король ♥ черви': 'K♥️',
        'Туз ♦ бубны': 'A♦️',
        '2 ♦ бубны': '2♦️',
        '3 ♦ бубны': '3♦️',
        '4 ♦ бубны': '4♦️',
        '5 ♦ бубны': '5♦️',
        '6 ♦ бубны': '6♦️',
        '7 ♦ бубны': '7♦️',
        '8 ♦ бубны': '8♦️',
        '9 ♦ бубны': '9♦️',
        '10 ♦ бубны': '10♦️',
        'Валет ♦ бубны': 'J♦️',
        'Дама ♦ бубны': 'Q♦️',
        'Король ♦ бубны': 'K♦️',
        'Туз ♣ трефы': 'A♣️',
        '2 ♣ трефы': '2♣️',
        '3 ♣ трефы': '3♣️',
        '4 ♣ трефы': '4♣️',
        '5 ♣ трефы': '5♣️',
        '6 ♣ трефы': '6♣️',
        '7 ♣ трефы': '7♣️',
        '8 ♣ трефы': '8♣️',
        '9 ♣ трефы': '9♣️',
        '10 ♣ трефы': '10♣️',
        'Валет ♣ трефы': 'J♣️',
        'Дама ♣ трефы': 'Q♣️',
        'Король ♣ трефы': 'K♣️'
    };

    let existingPlayerCards = [];
    let existingDealerCards = [];
    const playerCardCounts = {};
    const dealerCardCounts = {};

    function addCardToArray(cardKey, card, cardArray, cardCounts) {
        // Увеличиваем счётчик для каждой уникальной карты
        if (!cardCounts[cardKey]) {
            cardCounts[cardKey] = 0;
        }
        cardCounts[cardKey]++;

        // Добавляем карту в массив, если она ещё не была добавлена
        cardArray.push({key: cardKey, card: card, index: cardCounts[cardKey]});
    }


    function updateGame(data) {
        if (!data.show_dealer_cards) {
            $dealerCards.html(data.dealer_cards.join(', '));
            $dealerScore.html('<b>Сумма: </b>' + data.dealer_score);
        } else {
            $dealerCards.html(data.dealer_cards[0] + ', *');
            $dealerScore.html('<b>Сумма:</b> *');
        }

        $playerHands.html(data.player_hands.map((hand, index) =>
            `<b>Рука ${index + 1}:</b> ${hand.join(', ')}`).join('<br>'));
        $playerScores.html('<b>Суммы:</b> ' + data.player_scores.join(', '));

        data.player_hands.forEach((hand, handIndex) => {
            hand.forEach((card, cardIndex) => {
                const cardKey = `${handIndex}-${cardIndex}`;
                if (!existingPlayerCards.some(c => c.key === cardKey)) {
                    addCardToArray(cardKey, card, existingPlayerCards, playerCardCounts);
                    const shortName = cardShortNames[card] || card;
                    const $cardDiv = $('<div>').addClass('card');
                    const $topLeft = $('<div>').addClass('top-left').text(shortName);
                    const $bottomRight = $('<div>').addClass('bottom-right').text(shortName);
                    if (shortName.includes('♠️') || shortName.includes('♣️')) {
                        $topLeft.css('color', 'black');
                        $bottomRight.css('color', 'black');
                    } else if (shortName.includes('♥️') || shortName.includes('♦️')) {
                        $topLeft.css('color', 'red');
                        $bottomRight.css('color', 'red');
                    }

                    $cardDiv.append($topLeft, $bottomRight);
                    setTimeout(() => {
                        $playerCardsContainer.append($cardDiv);
                        setTimeout(() => {
                            $cardDiv.addClass('animate');
                        }, 50);
                    }, cardIndex * 150);
                }
            });
        });

        data.dealer_cards.forEach((card, cardIndex) => {
            const cardKey = `dealer-${cardIndex}`;
            if (!existingDealerCards.some(c => c.key === cardKey)) {
                addCardToArray(cardKey, card, existingDealerCards, dealerCardCounts);
                const shortName = cardShortNames[card] || card;
                const $cardDiv = $('<div>').addClass('card');
                const $topLeft = $('<div>').addClass('top-left').text(shortName);
                const $bottomRight = $('<div>').addClass('bottom-right').text(shortName);
                if (shortName.includes('♠️') || shortName.includes('♣️')) {
                    $topLeft.css('color', 'black');
                    $bottomRight.css('color', 'black');
                } else if (shortName.includes('♥️') || shortName.includes('♦️')) {
                    $topLeft.css('color', 'red');
                    $bottomRight.css('color', 'red');
                }

                $cardDiv.append($topLeft, $bottomRight);
                setTimeout(() => {
                    $dealerCardsContainer.append($cardDiv);
                    setTimeout(() => {
                        $cardDiv.addClass('animate');
                    }, 50);
                }, cardIndex * 250);
            }
        });

        if (data.game_over) {
            $result.html('<b>Результат</b>: ' + data.result.join(', ') + '<br><b>Был ли дабл:</b> ' + (data.double_check ? 'да' : 'нет'));
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

            if (data.can_split === true) {
                $split.removeClass('btn-outline-info').addClass('btn-info').prop('disabled', !data.can_split);
            } else {
                $split.removeClass('btn-info').addClass('btn-outline-info').prop('disabled', !data.can_split);
            }
        }
    }

    $start.click(function () {
        const decksCount = $('#decks-count').val();
        $dealerCardsContainer.empty();
        $playerCardsContainer.empty();
        existingPlayerCards = [];
        existingDealerCards = [];
        console.log(existingPlayerCards)
        $.post('/blackjack/start', {decks_count: decksCount}, function (data) {
            $split.removeClass('btn-info').addClass('btn-outline-info');
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
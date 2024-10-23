$(document).ready(function () {
    const $dealerCards = $('#dealer-cards');
    const $dealerScore = $('#dealer-score');
    const $playerHands = $('#player-hands');
    const $playerCardsContainer = $('#player-cards-container');
    const $playerCardsContainer2 = $('#player-cards-container-2');
    const $dealerCardsContainer = $('#dealer-cards-container');
    const $playerScores = $('#player-scores');
    const $result = $('#result');
    const $win = $('#win');
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
        if (!cardCounts[cardKey]) {
            cardCounts[cardKey] = 0;
        }
        cardCounts[cardKey]++;

        cardArray.push({key: cardKey, card: card, index: cardCounts[cardKey]});
    }

    function handlePlayerWin() {
        confetti({
            particleCount: 200,
            angle: 60,
            spread: 70,
            origin: {x: -0.1, y: 0.7}
        });

        confetti({
            particleCount: 200,
            angle: 120,
            spread: 70,
            origin: {x: 1.1, y: 0.7}
        });
    }

    function handlePlayerWinSmall() {
        confetti({
            particleCount: 150,
            angle: 60,
            spread: 50,
            origin: {x: -0.1, y: 0.9}
        });

        confetti({
            particleCount: 150,
            angle: 120,
            spread: 50,
            origin: {x: 1.1, y: 0.9}
        });
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
            const $targetContainer = handIndex === 0 ? $playerCardsContainer : $('#player-cards-container-2');

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
                        $targetContainer.append($cardDiv);
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
                }, cardIndex * 150);
            }
        });

        if (data.game_over) {
            console.log(data.result, data.win)
            $result.html('<b>Результат</b>: ' + data.result.join(', ') + '<br><b>Был ли дабл:</b> ' + (data.double_check ? 'да' : 'нет'));
            $win.html('<b>Выигрыш</b>: ' + data.win);

            $.post('/blackjack/end', {win: data.win}, function (response) {
                if (response.success) {
                    $('#balance-int').text(response.new_balance);
                }
            });

            $hit.add($hit2).add($double).add($split).add($stand).add($stand2).prop('disabled', true);

            if (data.result.includes('Игрок')) {
                setTimeout(handlePlayerWin, 1000);
            }
            if (data.result.includes('Блэкджэк у игрока')) {
                setTimeout(handlePlayerWin, 1000);
                setTimeout(handlePlayerWinSmall, 1500);
            }
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
        if (data.player_hands[0].length > 2 || (data.player_hands.length > 1 && data.player_hands[1].length > 1)) {
            $split.prop('disabled', true);
            $double.prop('disabled', true);
        } else {
            $split.prop('disabled', !data.can_split);
        }
    }

    $start.click(function () {
        const bet = parseInt($('#bet').val());
        const decksCount = $('#decks-count').val();

        $.get('/check_balance', function (data) {
            if (data.error) {
                alert(data.error);
            } else {
                const balanceInt = parseInt(data.balance);
                if (balanceInt < bet) {
                    alert('Insufficient balance');
                    return;
                }

                const newBalance = balanceInt - bet;
                $('#balance-int').text(newBalance);

                $dealerCardsContainer.empty();
                $playerCardsContainer.empty();
                $playerCardsContainer2.empty();
                existingPlayerCards = [];
                existingDealerCards = [];

                $.post('/blackjack/start', {bet: bet, decks_count: decksCount}, function (data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        $split.removeClass('btn-info').addClass('btn-outline-info');
                        updateGame(data);
                        if (!data.game_over) {
                            $hit.add($hit2).add($double).add($stand).add($stand2).prop('disabled', false);
                            $hit2.add($stand2).hide();
                        }
                    }
                });
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
            const firstHandNewCard = data.player_hands[0][1];
            const shortNameFirstHand = cardShortNames[firstHandNewCard] || firstHandNewCard;

            const $firstHandLastCard = $playerCardsContainer.find('.card:last');
            $firstHandLastCard.find('.top-left, .bottom-right').text(shortNameFirstHand);

            if (shortNameFirstHand.includes('♠️') || shortNameFirstHand.includes('♣️')) {
                $firstHandLastCard.find('.top-left').css('color', 'black');
                $firstHandLastCard.find('.bottom-right').css('color', 'black');
            } else if (shortNameFirstHand.includes('♥️') || shortNameFirstHand.includes('♦️')) {
                $firstHandLastCard.find('.top-left').css('color', 'red');
                $firstHandLastCard.find('.bottom-right').css('color', 'red');
            }

            const secondHandFirstCard = data.player_hands[1][0];
            const shortNameSecondHand = cardShortNames[secondHandFirstCard] || secondHandFirstCard;

            const $secondHandCardDiv = $('<div>').addClass('card');
            const $topLeftSecondHand = $('<div>').addClass('top-left').text(shortNameSecondHand);
            const $bottomRightSecondHand = $('<div>').addClass('bottom-right').text(shortNameSecondHand);

            $secondHandCardDiv.append($topLeftSecondHand, $bottomRightSecondHand);
            $('#player-cards-container-2').append($secondHandCardDiv);

            if (shortNameSecondHand.includes('♠️') || shortNameSecondHand.includes('♣️')) {
                $secondHandCardDiv.find('.top-left').css('color', 'black');
                $secondHandCardDiv.find('.bottom-right').css('color', 'black');
            } else if (shortNameSecondHand.includes('♥️') || shortNameSecondHand.includes('♦️')) {
                $secondHandCardDiv.find('.top-left').css('color', 'red');
                $secondHandCardDiv.find('.bottom-right').css('color', 'red');
            }

            $('#player-cards-container-2 .card:first').remove();

            updateGame(data);
        });
    });
})
;
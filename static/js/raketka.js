let coefElement = document.getElementById('current-coef');
let realTimeCoef = document.getElementById('real-time-coef');
let stopButton = document.getElementById('stop-rocket');
let startButton = document.querySelector('#raketka-form button[type="submit"]');
let ctx = document.getElementById('flightChart').getContext('2d');
let flightData = {
    labels: [],
    datasets: [{
        label: 'Траектория полета ракеты',
        borderColor: 'rgb(97,203,109)',
        data: [],
        fill: false,
        tension: 0.3
    }]
};

let chart = new Chart(ctx, {
    type: 'line',
    data: flightData,
    options: {
        scales: {
            x: {
                title: {display: true, text: 'Время'}
            },
            y: {
                beginAtZero: true,
                title: {display: true, text: 'Коэффициент'}
            }
        }
    }
});

function resetFlightChart() {
    flightData.labels = [];
    flightData.datasets[0].data = [];
    chart.update();
}

let rocketInterval;
let currentCoef = 1.00;

function animateRocketFlight(crashCoef, autoStop, callback) {
    let t = 0;
    rocketInterval = setInterval(() => {
        t += 1;
        currentCoef = 1 + Math.pow(t / 100, 2);

        coefElement.innerHTML = `Коэффициент: ${currentCoef.toFixed(2)}`;
        realTimeCoef.innerHTML = currentCoef.toFixed(2);

        flightData.labels.push(t);
        flightData.datasets[0].data.push(currentCoef);
        chart.update();

        if (currentCoef >= autoStop || currentCoef >= crashCoef) {
            clearInterval(rocketInterval);
            stopButton.style.display = 'none';
            startButton.style.display = 'flex';
            callback(currentCoef);
        }
    }, 150);
}

document.getElementById('raketka-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const bet = document.getElementById('bet').value;
    const auto_stop = parseFloat(document.getElementById('auto_stop').value);

    resetFlightChart();

    document.getElementById('result').innerHTML = '';

    stopButton.style.display = 'flex';
    startButton.style.display = 'none';

    fetch('/raketka/play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({bet: bet, auto_stop: auto_stop})
    })
        .then(response => response.json())
        .then(data => {
            const crashCoef = data.coef;

            animateRocketFlight(crashCoef, auto_stop, (finalCoef) => {
                document.getElementById('result').innerHTML = `
                    <p>${data.message}</p>
                    <p>Баланс: ${data.balance}</p>
                `;
            });
        });
});

stopButton.addEventListener('click', function () {
    clearInterval(rocketInterval);
    stopButton.style.display = 'none';
    startButton.style.display = 'flex';
    document.getElementById('result').innerHTML = `
            <p>Вы остановили ракету на коэффициенте ${currentCoef.toFixed(2)}</p>
            <p>Ваш выигрыш: ${(currentCoef * document.getElementById('bet').value).toFixed(2)} токенов</p>
        `;
});

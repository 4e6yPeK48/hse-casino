document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        let flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(function (message) {
            message.style.display = 'none';
        });
    }, 7000);
});
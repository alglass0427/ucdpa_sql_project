document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded.');
});


setTimeout(function() {
    var flashMessages = document.getElementsByClassName('flash-message');
    for (var i = 0; i < flashMessages.length; i++) {
        flashMessages[i].style.display = 'none';
    }
}, 3000); // 3000 milliseconds = 5 seconds


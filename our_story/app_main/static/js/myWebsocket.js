$(function() {
    var $username = $('input[name="username"]').val();
    var websocket = new WebSocket('ws://' + window.location.host +'/'+ $username + '/');

    websocket.addEventListener('close', function(e) {
        console.log('close')
    })
    websocket.addEventListener('message', function(e) {
        console.log('message')
    })
});
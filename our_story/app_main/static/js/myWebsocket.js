$(function() {
    var $username = $('input[name="username"]').val();
    var websocket = new WebSocket('ws://' + window.location.host +'/'+ $username + '/');

    websocket.addEventListener('close', function(e) {
        console.log('close')
    })
    websocket.addEventListener('message', function(e) {
        var data = JSON.parse(e.data);
        var $friend = $('a.btn-chatting-start').find('span#'+data['user']);
        var $unread = $('#chat-index-unread');

        $friend.parent().parent().find('#chat-index-last_message').html(data['last_message']);
        if (data['unread'] != 0) {
            $friend.parent().parent().find('#chat-index-unread').addClass('bg-danger').addClass('py-auto').addClass('p-1').html(data['unread']);
        }
    })
});
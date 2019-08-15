$(function() {
    var $document = $(document);
    $document.scrollTop($document.height());

    var participant = window.location.pathname.replace('/chat/message/', '');
    var chat_websocket = new WebSocket('ws://'+ window.location.host+'/chat/'+participant);

    // web server 에서 받은 메시지
    chat_websocket.addEventListener('message', function(e) {
        var $my_layout = $('#my-layout');
        var $friend_layout = $('#friend-layout');
        var data = JSON.parse(e.data);

        console.log(data['q']);
        if (data['q'] == 'Accept') {
            if (!data['left'])$('.unread').html('');
            return false;
        }
        console.log(data['created'])

        if ($('input[name="username"]').val() === data['from_user']){
            console.log(data['left'])
            if (data['left']) $my_layout.find('.unread').html('1');
            $my_layout.find('.mytime').html(data['created']);
            $my_layout.find('.myMsg').html(data['content']);

            $('.message-field').append($my_layout.html());
        } else {
            $friend_layout.find('.yourtime').html(data['created']);
            $friend_layout.find('.yourMsg').html(data['content']);

            $('.message-field').append($friend_layout.html());
        }
        $document.scrollTop($document.height());
    })

    $('.footer button').click(function() {
        var $content = $('input[name="message-content"]');
        chat_websocket.send(JSON.stringify({
            'content': $content.val(),
        }))
        $content.val('');
    });
})
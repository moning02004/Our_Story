$(document).ready(function() {
    var $chat_window = $('#chat-window');
    var $btn_chatting_start = $('.btn-chatting-start');
    var $btn_chatting_close = $('.btn-chatting-close');

    $btn_chatting_start.click(function() {
        if (screen.width < 1000) return false;
        var params = []
        params.push($(this).parent().parent().find('input.username').val())
        params.push($('input[name="username"]').val());
        params = params.join('/');
        console.log(params)
        newWindow = window.open("/chat/message/" + params, "", "width=400,height=600");
        return false
    });
    $btn_chatting_close.click(function() {
        $('.chat-message').addClass('d-none');
        $chat_window.html();
    })
});
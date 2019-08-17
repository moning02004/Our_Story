$(document).ready(function() {
    var $chat_window = $('#chat-window');
    var $btn_chatting_start = $('.btn-chatting-start');
    var $btn_chatting_close = $('.btn-chatting-close');

    $btn_chatting_start.click(function() {
        if (screen.width < 1000) return false;
        $(this).parent().find('#chat-index-unread').removeClass('bg-danger').removeClass('py-auto').removeClass('p-1');
        var params = []
        params.push($(this).find('span').attr('id'));
        params.push($('input[name="username"]').val());
        params = params.join('/');
        newWindow = window.open("/chat/message/" + params, "", "width=400,height=600");
    });
});
$(document).ready(function() {
    $('.heart').click(function() {
        console.log($(this).find('span').text());
        var $pk = $(this).find('span').text();
        $.ajax({
            url: '/post/heart/',
            data: {'pk': $pk},
            dataType: 'json',
            type: 'POST',
            success: function(data){
                if (data['message'] == 'OK'){
                    location.reload();
                }
            }
        });
    });

    $('.btn-remove').click(function() {
        if (!confirm('삭제하시겠습니까?')) return false;
        var $pk = $('#pk').text();
        $.ajax({
            url: '/post/remove/',
            data: {'pk': $pk},
            dataType: 'json',
            type: 'POST',
            success: function(data) {
                if (data['message'] === "OK") location.replace('/dashboard/');

            }
        });
    });

    $('.btn-comment').click(function() {
        if (!confirm('작성하시겠습니까?')) return false;
        var $pk = $('#pk').text();
        var $content = $('input[name="content"]');
        $.ajax({
            url: '/post/comment/',
            data: {'pk': $pk, 'content': $content.val()},
            dataType: 'json',
            type: 'POST',
            success: function(data) {
                if (data['message'] == 'NO') {
                    alert('문제가 발생했습니다.');
                    return false;
                }
                var $layout = $('#comment-layout');
                $layout.find('#author').html(data['author']);
                $layout.find('#content').html(data['content']);
                $layout.find('#created').html(data['created']);
                console.log($layout.html())
                $content.val('');
                var $field = $('#comment-field');
                $field.prepend($layout.html());

            }
        });
    });
});
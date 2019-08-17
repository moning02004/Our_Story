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
                $content.val('');
                var $field = $('#comment-field');
                $field.prepend($layout.html());

            }
        });
    });

    $('#btn-option').click(function() {
        $(this).find('i').toggleClass('fa-chevron-down');
        $(this).find('i').toggleClass('fa-chevron-up');
    });

    $('#post-image-text').click(function() {
        $('#post-image').click();
    });
    $('#post-image').change(function() {
        if ($(this).get(0).files.length <= 0) return false;

        var files = [];
        for (var i=0; i < $(this).get(0).files.length; i++){
            console.log($(this).get(0).files[i].name);
            files.push($(this).get(0).files[i].name);
        }
        $('#post-image-text').html(files.join(", "));
    });
});
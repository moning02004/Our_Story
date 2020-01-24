$(document).ready(function() {
    $('.heart').click(function() {
        let $origin = $(this);
        let $pk = $(this).parent().attr('id');

        $.ajax({
            url: '/post/heart/',
            data: {'pk': $pk},
            dataType: 'json',
            type: 'POST',
            success: function(data){
                if (data['message'] == 'OK'){
                    $origin.children('i').toggleClass('text-danger');
                    $origin.children('i').toggleClass('fas');
                    $origin.children('i').toggleClass('far');
                    number = Number($origin.children('sup').text());
                    number += ($origin.children('i').hasClass('fas')) ? 1 : -1;
                    $origin.children('sup').text(number);
                }
            }
        });
    });

    $('.btn-remove').click(function() {
        if (!confirm('삭제하시겠습니까?')) return false;

        let $pk = $(this).parent().parent().attr('id');
        console.log($pk);
        $.ajax({
            url: '/post/remove/',
            data: {'pk': $pk},
            dataType: 'json',
            type: 'POST',
            success: function(data) {
                if (data['message'] === "OK") {
                    console.log("dadsf")
                    location.replace('/dashboard/');
                }
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
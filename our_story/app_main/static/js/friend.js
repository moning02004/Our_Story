$(document).ready(function() {
    var $btn_add = $('.btn-add');
    $btn_add.click(function() {
        $.ajax({
            url: '/friend/add/',
            data: {'username': $(this).val()},
            type: 'POST',
            success: function(data) {
                location.reload();
            },
            error: function() {
                alert('에러가 발생했습니다.');
            }
        })
    });

    var $btn_release = $('.btn-release');
    $btn_release.click(function() {
        $.ajax({
            url: '/friend/release/',
            data: {'username': $(this).val()},
            type: 'POST',
            success: function(data) {
                location.reload();
            },
            error: function() {
                alert('에러가 발생했습니다.');
            }
        })
    });

});
$(document).ready(function() {
    var $btn_add = $('.btn-add');
    $btn_add.click(function() {
        $.ajax({
            url: '/friend/add/',
            data: {'username': $(this).val()},
            dataType: 'json',
            type: 'POST',
            success: function(data) {
                if (data['message'] == 'OK') {
                    location.reload();
                }
            }
        })
    });

    var $btn_release = $('.btn-release');
    $btn_release.click(function() {
        $.ajax({
            url: '/friend/release/',
            data: {'username': $(this).val()},
            dataType: 'json',
            type: 'POST',
            success: function(data) {
                if (data['message'] == 'OK') {
                    location.reload();
                }
            }
        })
    });

});
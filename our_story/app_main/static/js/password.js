$(document).ready(function() {
    var $password = $('#password');
    var $password2 = $('#password2');
    $password.keyup(function() {
        var $check_icon = $('#check-password i');
        var pattern = /(?=.*[0-9])(?=.*[a-z]){8}/i;
        if (pattern.test($(this).val())){
            $check_icon.removeClass('fa-times');
            $check_icon.removeClass('text-danger');
            $check_icon.addClass('fa-check');
            $check_icon.addClass('text-primary');
        } else {
            $check_icon.removeClass('fa-check');
            $check_icon.removeClass('text-primary');
            $check_icon.addClass('fa-times');
            $check_icon.addClass('text-danger');
        }
         $password2.keyup();
    });

    $password2.keyup(function() {
        var $check_icon = $('#check-password2 i');
        if ($password.val() === $(this).val()){
            $check_icon.removeClass('fa-times');
            $check_icon.removeClass('text-danger');
            $check_icon.addClass('fa-check');
            $check_icon.addClass('text-primary');
        } else {
            $check_icon.removeClass('fa-check');
            $check_icon.removeClass('text-primary');
            $check_icon.addClass('fa-times');
            $check_icon.addClass('text-danger');
        }
    });

});
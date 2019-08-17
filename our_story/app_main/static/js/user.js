$(document).ready(function() {
    // register
    var username_regex = /[0-9a-zA-Z]/g;

    $('input[value="가입"]').click(function() {
        var address_regex = /[가-힣]/g;
        var bName = ($('input[name="fname"]').val() != '' && $('input[name="lname"]').val() != '');
        var bUsername = $('#check-username > i').hasClass('fa-check');
        var bPassword = $('#check-password > i').hasClass('fa-check');
        var bPassword2 = $('#check-password2 > i').hasClass('fa-check');
        var bAddress = address_regex.test($('input[name="address"]').val());
        var bSex = $('input[name="sex"]').is(':checked');
        var $birth = $('#birth');

        if (bName && bUsername && bPassword && bPassword2 && bAddress && bSex) {
            $('form#register').submit()
            return false;
        }
        alert("Check the information");
        return false;
    })

    // check username
    var $check_username = $('#check-username');
    var $origin_check = $check_username.html();
    $check_username.click(function() {
        var $username = $('#username').val();
        if ($username === '' || !username_regex.test($username)) {
            alert('영어로 입력되어 있는지, 빈칸인지 확인해주십시오.');
            $('#username').focus();
            return false;
        }
        $.ajax({
            url: '/user/check_username/',
            data: {'username': $username},
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data['message'] == 'OK' ) {
                    $check_username.find('i').removeClass('fa-user');
                    $check_username.find('i').removeClass('fa-times');
                    $check_username.find('i').addClass('fa-check');
                    $check_username.find('i').addClass('text-primary');
                } else {
                    $check_username.find('i').removeClass('fa-user');
                    $check_username.find('i').removeClass('fa-check');
                    $check_username.find('i').addClass('fa-times');
                    $check_username.find('i').addClass('text-danger');
                }
            }
        });
    });
    $('input[name="username"]').keyup(function() {
        $check_username.html($origin_check);
    });

});
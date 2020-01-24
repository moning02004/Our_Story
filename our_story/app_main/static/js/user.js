$(document).ready(function() {
    // register
    let username_regex = /[0-9a-zA-Z]/g;

    $('input[value="가입"]').click(function() {
        let bUsername = $('#check-username > i').hasClass('fa-check');
        let bPassword = $('#check-password > i').hasClass('fa-check');
        let bPassword2 = $('#check-password2 > i').hasClass('fa-check');
        let bEmail = ($('#tel').value != '') ? true : false;
        let bName = ($('#name').value != '') ? true : false

        if (bName && bUsername && bPassword && bPassword2 && bEmail) {
            $('form#register').submit();
            return false;
        }
        alert("Check the information");
        return false;
    })

    // check username
    let $check_username = $('#check-username');
    let $origin_check = $check_username.html();
    $check_username.click(function() {
        let $username = $('#username').val();
        if ($username === '' || !username_regex.test($username)) {
            alert('영어로 입력되어 있는지, 빈칸인지 확인해주십시오.');
            $('#username').focus();
            return false;
        }
        $.ajax({
            url: '/user/check_username/',
            data: {'username': $username},
            type: 'POST',
            success: function(data) {
                $check_username.find('i').removeClass('fa-user');
                $check_username.find('i').removeClass('fa-times');
                $check_username.find('i').addClass('fa-check');
                $check_username.find('i').addClass('text-primary');
            },
            error: function() {
                $check_username.find('i').removeClass('fa-user');
                $check_username.find('i').removeClass('fa-check');
                $check_username.find('i').addClass('fa-times');
                $check_username.find('i').addClass('text-danger');
            }
        });
    });

    $('input[name="username"]').keyup(function() {
        $check_username.html($origin_check);
    });

});
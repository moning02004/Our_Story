$(document).ready(function() {
    // register
    var $birth = $('#birth');
    $('form#register').submit(function() {
        var address_regex = /[가-힣]/g;

        var bName = ($('input[name="fname"]').val() != '' && $('input[name="lname"]').val() != '');
        var bUsername = $('#check-username > i').hasClass('fa-check');
        var bPassword = $('#check-password > i').hasClass('fa-check');
        var bPassword2 = $('#check-password2 > i').hasClass('fa-check');
        var bAddress = address_regex.test($('input[name="address"]').val());
        var bSex = $('input[name="sex"]').is(':checked');

        if (bName && bUsername && bPassword && bPassword2 && bAddress && bSex) {
            return true;
        }
        alert("Check the information");
        return false;
    });


    $birth.datepicker({
        dateFormat: 'yy-mm-dd',
        yearRange: '1980:',
        changeMonth: true,
        changeYear: true,
        prevText: '이전 달',
        nextText: '다음 달',
        monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        monthNamesShort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        dayNames: ['일', '월', '화', '수', '목', '금', '토'],
        dayNamesShort: ['일', '월', '화', '수', '목', '금', '토'],
        dayNamesMin: ['일', '월', '화', '수', '목', '금', '토'],
        showMonthAfterYear: true,
        yearSuffix: '년'
    });
    $birth.keyup(function() {
        $(this).val('');
    })


    // check username
    var $check_username = $('#check-username');
    var $origin_check = $check_username.html();
    $check_username.click(function() {
        var $username = $('#username').val();
        if ($username === '') return false;
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
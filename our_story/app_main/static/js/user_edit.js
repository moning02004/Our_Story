$(document).ready(function() {
    var $profile_pic = $('#profile-picture');
    $profile_pic.change(function(e) {
        if ($(this).get(0).files.length <= 0){
            return false;
        }
        readURL(this);
    });

    let $previewer = $('.previewer');
    $previewer.click(function() {
        window.open($previewer.find('img').attr('src'), '_blank');
    });
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $previewer.attr('hidden', false);
                $previewer.find('img').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    var $btn_status = $('#chg-status');
    $btn_status.click(function() {
        $(this).text(($(this).text() == "상태 메시지") ? "저장" : "상태 메시지");

        if ($(this).text() == "상태 메시지") {
            let $status = $("input[name='status']");
            $.ajax({
                url: '/user/status/',
                data: {'status': $status.val()},
                method: 'POST',
                success: function(data) {
                    $('#status').css('display', 'block');
                    $('#chg-input').css('display', 'none');
                    $('#status').text(data);
                    $status.val(data);
                },
                error: function() {
                    alert('에러가 발생했습니다.')
                }
            });
        } else {
            $('#status').css('display', 'none');
            $('#chg-input').css('display', 'inline');
        }
    });
});

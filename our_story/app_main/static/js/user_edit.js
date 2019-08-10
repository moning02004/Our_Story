$(document).ready(function() {
    var $profile_pic = $('#profile-picture');
    $profile_pic.change(function(e) {
        if ($(this).get(0).files.length <= 0){
            return false;
        }
        readURL(this);
    });

    function readURL(input) {
        var $previewer = $('#previewer');
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $previewer.attr('hidden', false);
                $previewer.find('img').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

});
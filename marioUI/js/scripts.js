jQuery(document).ready(function () {
    var user = getCookie('username');
    var pass = getCookie('password');

    if (user != null && user != "" && pass != null && pass != "") {
        $('.page-container form').submit();
    }

    $('.page-container form').submit(function () {
        var username = $(this).find('.username').val();
        var password = $(this).find('.password').val();
        if (username == '') {
            $(this).find('.error').fadeOut('fast', function () {
                $(this).css('top', '27px');
            });
            $(this).find('.error').fadeIn('fast', function () {
                $(this).parent().find('.username').focus();
            });
            return false;
        } else if (password == '') {
            $(this).find('.error').fadeOut('fast', function () {
                $(this).css('top', '96px');
            });
            $(this).find('.error').fadeIn('fast', function () {
                $(this).parent().find('.password').focus();
            });
            return false;
        } else {
            setCookie("username", username, 1);
            setCookie("password", username, 1);
        }
    });

    $('.page-container form .username, .page-container form .password').keyup(function () {
        $(this).parent().find('.error').fadeOut('fast');
    });

});

function setCookie(c_name, value, expiredays) {
    var exdate = new Date()
    exdate.setDate(exdate.getDate() + expiredays)
    document.cookie = c_name + "=" + escape(value) +
        ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString())
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=")
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1
            c_end = document.cookie.indexOf(";", c_start)
            if (c_end == -1) c_end = document.cookie.length
            return unescape(document.cookie.substring(c_start, c_end))
        }
    }
    return ""
}
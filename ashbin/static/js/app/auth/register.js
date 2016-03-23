/**
 * Created by admin on 2016/3/21.
 */
var Script = function(){
    $.validator.setDefaults({
        submitHandler: function() {
            jQuery.ajax({
                url: window.location.href,   // 提交的页面
                data: $('form').serialize(), // 从表单中获取数据
                type: "POST",                   // 设置请求类型为"POST"，默认为"GET"
                success: function(data) {
                    console.log(data);
                    window.location.href = data;
                },
                error: function(res) {
                    var usernameInput = $('#username').addClass('error');
                    usernameInput.after('<label class="error">' + res.responseJSON.message + '</label>');
                    usernameInput.on('input', function(){
                        usernameInput.removeClass('error');
                        usernameInput.next('label').remove();
                    })

                }
            });
        }
});
    $(document).ready(function() {

    $("#signupForm").validate({
        rules: {
            username: {
                required: true,
                minlength: 2
            },
            password: {
                required: true,
                minlength: 6
            },
            confirm_password: {
                required: true,
                minlength: 6,
                equalTo: "#password"
            },
            agree: "required"
        },
        messages: {
            username: {
                required: "Please enter a username",
                minlength: "Your username must consist of at least 2 characters"
            },
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 6 characters long"
            },
            confirm_password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 6 characters long",
                equalTo: "Please enter the same password as above"
            },
            agree: "Please accept our policy"
        }
        });

    });
}();

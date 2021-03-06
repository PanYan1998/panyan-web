define(['jquery', 'validator', 'common'],
function($, validator, common) { 
    return {
        init: function() {
            var email = 
            validator.bind($("main#register #email"),
                           $("main#register #email").next(),
                           function(val) {return val.match(common.email_pattern);},
                           "< 请输入邮箱",
                           "< 邮箱格式不对");

            var username =
            validator.bind($("main#register #username"),
                           $("main#register #username").next(),
                           function(val) {return val.match(common.username_pattern);},
                           "< 请输入帐号",
                           "< 2-20个字符，字母、数字、下划线，字母开头");

            var password =
            validator.bind($("main#register #password"),
                           $("main#register #password").next(),
                           function(val) {return val.match(common.password_pattern);},
                           "< 请输入密码",
                           "< 密码格式不对");

            var password_again =
            validator.bind($("main#register #password_again"),
                           $("main#register #password_again").next(),
                           function(val) {return (val==$("#password").val());},
                           "< 请再次输入密码",
                           "< 密码不匹配");

            $("main#register").submit(function(event) {
                // 输入有误无法提交
                if (!(email.valid && username.valid && password.valid && password_again.valid)) {
                    // stop form from submitting normally
                    event.preventDefault();
                }
            });

            // 进入注册页面，默认由email输入框获取焦点
            $("main#register #email").focus();
        }
    }
});

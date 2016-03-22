/**
 * Created by qitian on 2016/3/18.
 */
$(document).ready(function()
        {
            $('form').submit(function(){
                jQuery.ajax({
                    url: window.location.href,   // 提交的页面
                    data: $('form').serialize(), // 从表单中获取数据
                    type: "POST",                   // 设置请求类型为"POST"，默认为"GET"
                    success: function(data) {
                        console.log(data);
                        window.location.href = data;
                    }
                });
                return false;
            });
        });
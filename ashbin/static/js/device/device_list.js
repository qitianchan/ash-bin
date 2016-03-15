/**
 * Created by admin on 2016/3/15.
 */
$(document).ready(function(){
    $('#delete-device').click(function(){
        if(confirm('是否删除')){
            console.log('delete')
        }else {
            console.log('abort')
        }
    })
});
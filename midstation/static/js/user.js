/**
 * Created by qitian on 2015/9/10.
 */

console.log('wtf');
$.fn.toggleDisabled = function() {
    return this.each(function() {
        var $this = $(this);
        if ($this.attr('disabled')) $this.removeAttr('disabled');
        else $this.attr('disabled', 'disabled');
    });
};

$(document).ready(function() {
        //$('#edit').onclick(function() {
        //$('#user_profile_info_fieldset').toggleDisabled();

    $('p').click(function(){
        this.hide()
    })
    }

);

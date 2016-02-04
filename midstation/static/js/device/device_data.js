/**
 * Created by qitian on 2016/2/1.
 */
$(document).ready(function(){
    namespace = '/device';

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // use mac for eventName
    var eventName = $('#device-mac').text().replace(/[ ]/g,"");
    var send = function () {
        window.console.log('hello');
        socket.emit('test', {data: 'hello'})
    };
    window.setInterval(send, 2000);
    //
    socket.on(eventName, function(msg) {

        $('#device-data').prepend("<tr>" +
            "<td>" + msg.create_time + "</td>" +
            "<td>" + msg.occupancy + " %</td>" +
            "<td>" + msg.temperature + " ℃</td>" +
            "<td>" + msg.electric_level + "</td></tr>");

    });
});
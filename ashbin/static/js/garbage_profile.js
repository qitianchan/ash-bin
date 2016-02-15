/**
 * Created by qitian on 2016/1/27.
 */
$(document).ready(function(){
    namespace = '/test'; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    });
    $('#emit').click(function(){
        window.console.log('emit');
        socket.emit('my event', {'data': 'hello'});
    });


    var map = new AMap.Map('container',{
        zoom: 10,
        center: [116.39,39.9]
    });

    AMap.service(["AMap.PlaceSearch"], function() {
        var placeSearch = new AMap.PlaceSearch({ //构造地点查询类
            pageSize: 1,
            pageIndex: 1,
            city: "020", //城市
            map: map//,
            //panel: "panel"
        });
        var i = 1000;

         var _onClick = function(e){
            socket.emit('my event', {'data': e.lnglat});
            var overlay = map.getAllOverlays(AMap.Marker);
            map.remove(overlay);
            new AMap.Marker({
              position : e.lnglat,
              map : map
            });
             //var lng = document.getElementById('longitude');
             //lng.value = e.lnglat.lng;
             //
             //var latitude = document.getElementById('latitude');
             //latitude.value = e.lnglat.lat;
             latlng.innerHTML = '<p>经纬度：（'+ e.lnglat.lng + ',' + e.lnglat.lat + ')</p>'
        };
        var clickListener;
        var bind = function(){

          clickListener = AMap.event.addListener(map, "click", _onClick);
        };
        document.getElementById('container').addEventListener('click', bind);

        //关键字查询
        var search = document.getElementById('search');
        search.onclick = function(){
            var addr = document.getElementById('addr').value;
            placeSearch.search(addr, function(status, result){
                if(status === 'complete') {
                    point = result.poiList.pois[0].location;
                    lat = point['lat'];
                    lng = point['lng'];
                }
            })
        };
    });
});

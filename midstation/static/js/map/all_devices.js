$(document).ready(function(){
    var map = new AMap.Map('container', {
        resizeEnable: true,
        center: [116.397428, 39.90923],
        zoom: 13
    });
    map.clearMap();  // 清除地图覆盖物
    var aj = $.ajax({
        url: 'devices_lnglat',
        type:'get',
        cache: false,
        dataType: 'json',
        success: function(res) {
            if (res.data) {
                var positions = [];
                $.each(res.data, function (i, item) {
                    var p = {};
                    p.lng = item.lng;
                    p.lat = item.lat;
                    positions.push(p)
                });
            }
        }
    });
    var markers = [{
        icon: 'http://webapi.amap.com/theme/v1.3/markers/n/mark_b1.png',
        position: [116.205467, 39.907761]
    }, {
        icon: 'http://webapi.amap.com/theme/v1.3/markers/n/mark_b2.png',
        position: [116.368904, 39.913423]
    }, {
        icon: 'http://webapi.amap.com/theme/v1.3/markers/n/mark_b3.png',
        position: [116.305467, 39.807761]
    }];
    // 添加一些分布不均的点到地图上,地图上添加三个点标记，作为参照
    markers.forEach(function(marker) {
        new AMap.Marker({
            map: map,
            icon: marker.icon,
            position: [marker.position[0], marker.position[1]],
            offset: new AMap.Pixel(-12, -36)
        });
    });
    var newCenter = map.setFitView();
    // 添加事件监听, 使地图自适应显示到合适的范围
    AMap.event.addDomListener(document.getElementById('setFitView'), 'click', function() {
        var newCenter = map.setFitView();
    });
});

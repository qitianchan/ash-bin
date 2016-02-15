$(document).ready(function(){
    var map = new AMap.Map('container', {
        resizeEnable: true,
        center: [116.397428, 39.90923],
        zoom: 13
    });
    map.clearMap();  // 清除地图覆盖物
    var _onClick = function() {
        // todo:点击显示数据
        var aj = $.ajax({
            url: 'device_data',
            type: 'get',
            cache: false,
            dataType: 'json',
            data: {device_id: this.device_id} ,
            success: function(res) {
                if (res.data) {
                    // todo: 用模态框显示数据
                    var inst = $('[data-remodal-id=modal]').remodal();

                    /**
                     * Opens the modal window
                     */
                    inst.open();
                }
            }
        })
    };

    var aj = $.ajax({
        url: 'devices_lnglat',
        type:'get',
        cache: false,
        dataType: 'json',
        success: function(res) {
            if (res.data) {
                var positions = [];
                var markers = [];
                $.each(res.data, function (i, item) {
                    var p = {};
                    p.lng = item.lng;
                    p.lat = item.lat;
                    p.occupancy = item.occupancy;
                    marker = {position: [p.lng, p.lat], device_id: item.device_id};
                    markers.push(marker);
                    positions.push(p)
                });

                markers.forEach(function(marker) {
                    temp = marker;
                    var temp_marker = new AMap.Marker({
                        map: map,
                        icon: marker.icon,
                        position: [marker.position[0], marker.position[1]],
                        offset: new AMap.Pixel(-12, -36)
                    });
                    device_id = marker.device_id;
                    AMap.event.addListener(temp_marker, 'click', _onClick, {device_id:device_id})
                });

                var newCenter = map.setFitView();
            }
        }
    });
});
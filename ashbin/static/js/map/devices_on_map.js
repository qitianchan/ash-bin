$(document).ready(function(){
    var cluster, markers = [];

    var map = new AMap.Map('container', {
        resizeEnable: true,
        center: [116.397428, 39.90923],
        zoom: 5
    });
    map.clearMap();  // 清除地图覆盖物
    var _onClick = function() {
        // todo: 跳转到设备详情页
    };
    var infoWindow = new AMap.InfoWindow({
                        isCustom: true,  //使用自定义窗体
                        offset: new AMap.Pixel(16, -45)
                    });
    // todo: 显示不同状态的垃圾桶标志， 超过80%的用红图标标志
    // todo: 设备在地图上的同步信息
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
                    var markerPosition = [p.lng, p.lat];
                    var marker = new AMap.Marker({
                        map: map,
                        position: markerPosition,
                        icon: item.icon,
                        offset: {x: -8,y: -34}
                    });
                    AMap.event.addListener(marker, 'click', function() {
                        infoWindow.open(map, marker.getPosition());
                    });
                        markers.push(marker);
                    var newCenter = map.setFitView();
                    //实例化信息窗体
                    var title = item.eui,
                    content = [];
                    content.push("Longitude: " + item.lng);
                    content.push("Latitude: " + item.lat);
                    content.push("Last Reading: " + item.create_time);
                    content.push("Filling Level: " + item.occupancy + '%');
                    content.push("Battery Level: " + item.battery + '%');
                    content.push("Temperature: " + item.temperature + '&#8451');
                    content.push("<a href=" + item.detail + ">More Information</a>");
                    marker.content = createInfoWindow(title, content.join("<br/>"));
                    marker.on('click', markerClick);
                    marker.emit('click', {target: marker});
                });


                addCluster(markers);
            }
        }
    });

    function markerClick(e) {
        infoWindow.setContent(e.target.content);
        infoWindow.open(map, e.target.getPosition());
    }

    //构建自定义信息窗体
    function createInfoWindow(title, content) {
        var info = document.createElement("div");
        info.className = "info";

        //可以通过下面的方式修改自定义窗体的宽高
        //info.style.width = "400px";
        // 定义顶部标题
        var top = document.createElement("div");
        var titleD = document.createElement("div");
        var closeX = document.createElement("img");
        top.className = "info-top";
        titleD.innerHTML = title;
        closeX.src = "http://webapi.amap.com/images/close2.gif";
        closeX.onclick = closeInfoWindow;

        top.appendChild(titleD);
        top.appendChild(closeX);
        info.appendChild(top);

        // 定义中部内容
        var middle = document.createElement("div");
        middle.className = "info-middle";
        middle.style.backgroundColor = 'white';
        middle.innerHTML = content;
        info.appendChild(middle);

        // 定义底部内容
        var bottom = document.createElement("div");
        bottom.className = "info-bottom";
        bottom.style.position = 'relative';
        bottom.style.top = '0px';
        bottom.style.margin = '0 auto';
        var sharp = document.createElement("img");
        sharp.src = "http://webapi.amap.com/images/sharp.png";
        bottom.appendChild(sharp);
        info.appendChild(bottom);
        return info;
    }

    //关闭信息窗体
    function closeInfoWindow() {
        map.clearInfoWindow();
    }
    function addCluster(markers) {
        if (cluster) {
            cluster.setMap(null);
        }
        map.plugin(["AMap.MarkerClusterer"], function() {
            cluster = new AMap.MarkerClusterer(map, markers);
        });
    }
});
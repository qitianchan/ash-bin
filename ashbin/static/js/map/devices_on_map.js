$(document).ready(function(){
    var map = new AMap.Map('container', {
        resizeEnable: true,
        center: [116.397428, 39.90923],
        zoom: 13
    });
    map.clearMap();  // 清除地图覆盖物
    var _onClick = function() {
        var aj = $.ajax({
            url: 'device_data',
            type: 'get',
            cache: false,
            dataType: 'json',
            data: {device_id: this.device_id} ,
            success: function(res) {
                if (res.data) {
                    var date = [];
                   var data = [];
                   $.each(res.data, function(i, item){
                       date.push(item.create_time);
                       data.push(item.occupancy);
                   });
                   var myChart = echarts.init(document.getElementById('chart'));
                    option = {
                        title: {
                            x: 'center',
                            text: '垃圾占用率'
                        },
                        legend: {
                            top: 'bottom',
                            data:['意向']
                        },
                        xAxis: [
                            {
                                type: 'category',
                                boundaryGap: false,
                                data: date
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value',
                                max: 100
                            }
                        ],
                        dataZoom: {
                            type: 'inside',
                            start: 40,
                            end: 100
                        },
                        series: [
                            {
                                name:'占用率',
                                type:'line',
                                smooth:true,
                                symbol: 'none',
                                stack: 'a',
                                areaStyle: {
                                    normal: {}
                                },
                                data: data
                            }
                        ]
                    };

                    // 使用刚指定的配置项和数据显示图表。
                    myChart.setOption(option);

                    var inst = $('[data-remodal-id=modal]').remodal();

                    /**
                     * Opens the modal window
                     */
                    inst.open();
                }
            }
        })
    };
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
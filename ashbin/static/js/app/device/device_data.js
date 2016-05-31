/**
 * Created by qitian on 2016/2/1.
 */
$(document).ready(function(){

    var ajax = $.ajax({
        url: window.location.href + '/resource',
        type: 'get',
        datatype: 'json',
        success: function(res) {
            var map = new AMap.Map('map-container', {
                resizeEnable: true,
                center: [res.lng, res.lat],
                zoom: 5
            });
            var marker = new AMap.Marker({
                        map: map,
                        position: [res.lng, res.lat],
                        icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
                        offset: {x: -8,y: -34}
                    });
             var newCenter = map.setFitView();
        }

    });


    namespace = '/device';
    var fillChart = echarts.init(document.getElementById('fill-level'));
    var temperatureChart = echarts.init(document.getElementById('temperature'));
    var batteryChart = echarts.init(document.getElementById('battery-level'));
    var date = [];
    var fillLevel = [];
    var temperature = [];
    var batteryLevel = [];

    var option = {
        title: {
            x: 'center',
            text: 'Fill Level'
        },
        legend: {
            data:['Fill Level','Battery']
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                return params[0].name + '<br />' + 'Fill Level：' + params[0].value + '%&nbsp&nbsp&nbsp&nbsp' + '<br/>';
            },
            axisPointer: {
                animation: true
            }
        },
        xAxis: [
            {
                type: 'category',
                name: 'Date Time',
                nameLocation: 'middle',
                nameGap: 20,
                nameTextStyle: {
                    color: '#7A7676',
                    fontSize: 16
                },
                boundaryGap: false,
                data: date
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: 'Fill Level',
                nameLocation: 'end',
                nameGap: 20,
                nameTextStyle: {
                    color: '#7A7676',
                    fontSize: 16
                },
                max: 120
                //boundaryGap: [0, '100%']
            }
        ],
        dataZoom: {
            type: 'inside',
            start: 60,
            end: 100
        },
        series: [
            {
                name:'fill level',
                type:'line',
                sampling: 'average',
                smooth:true,
                symbolSize: 8,
                data: fillLevel
            }
        ],
        textstyle: {
            color: '#333'
        },
        color: ['#6A7984']
    };
    var temperatureOption = {
        title: {
            x: 'center',
            text: 'Temperature'
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                return params[0].name + '<br />' + 'Temperature：' + params[0].value + '℃&nbsp&nbsp&nbsp&nbsp' + '<br/>';
            },
            axisPointer: {
                animation: true
            }
        },
        xAxis: [
            {
                type: 'category',
                name: 'Date Time',
                nameLocation: 'middle',
                nameGap: 20,
                nameTextStyle: {
                    color: '#7A7676',
                    fontSize: 16
                },
                boundaryGap: false,
                data: date
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: 'Temperature',
                nameLocation: 'end',
                nameGap: 20,
                nameTextStyle: {
                    color: '#7A7676',
                    fontSize: 16
                },
                //max: 120
                //boundaryGap: [0, '100%']
            }
        ],
        dataZoom: {
            type: 'inside',
            start: 60,
            end: 100
        },
        series: [
            {
                name:'temperature',
                type:'line',
                sampling: 'average',
                smooth:true,
                symbolSize: 8,
                data: temperature
            }
        ],
        textstyle: {
            color: '#333'
        },
        color: ['#6A7984']
    };

    var batteryOption = {
        title: {
            x: 'center',
            text: 'Battery'
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                return params[0].name + '<br />' + 'Battery：' + params[0].value + '%&nbsp&nbsp&nbsp&nbsp' + '<br/>';
            },
            axisPointer: {
                animation: true
            }
        },
        xAxis: [
            {
                type: 'category',
                name: 'Date Time',
                nameLocation: 'middle',
                nameGap: 20,
                nameTextStyle: {
                    color: '#7A7676',
                    fontSize: 16
                },
                boundaryGap: false,
                data: date
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: 'Battery',
                nameLocation: 'end',
                nameGap: 20,
                nameTextStyle: {
                    color: '#7A7676',
                    fontSize: 16
                },
                //max: 120
                //boundaryGap: [0, '100%']
            }
        ],
        dataZoom: {
            type: 'inside',
            start: 60,
            end: 100
        },
        series: [
            {
                name:'battery',
                type:'line',
                smooth:true,
                symbolSize: 8,
                data: batteryLevel
            }
        ],
        textstyle: {
            color: '#333'
        },
        color: ['#6A7984']
    };
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // use mac for eventName
    //var eventName = $('#device-mac').text().replace(/[ ]/g,"");
    var eventName = '01685DF0';
    //
    socket.on(eventName, function(msg) {
        $('#info-temperature').html(msg.temperature + '℃');
        $('#info-battery').html(msg.electric_level + '%');
        $('#info-occupancy').html(msg.occupancy + '%');
        $('#info-date').html('20' + msg.create_time.split(' ')[0].replace(/\//g, '-'));
        $('#info-time').html(msg.create_time.split(' ')[1]);
        $('#data-table > tbody').prepend("<tr>" +
            "<td>20" + msg.create_time.replace(/\//g, '-') + "</td>" +
            "<td>" + msg.occupancy + " %</td>" +
            "<td>" + msg.temperature + "℃</td>" +
            "<td>" + msg.electric_level + " %</td></tr>");

        date.push(msg.create_time);
        fillLevel.push(msg.occupancy);
        temperature.push(msg.temperature);
        batteryLevel.push(msg.electric_level);
        fillChart.setOption(option);
        temperatureChart.setOption(temperatureOption);
        batteryChart.setOption(batteryOption);
    });
    var aj = $.ajax({
        url: 'data_one_month',

        type:'get',
        cache: false,
        dataType: 'json',
        success: function(res) {
           if(res.data){
               //var date = [];
               //var data = [];
               if(res.data.length < 200){
                   option.dataZoom.start = 0;
                   temperatureOption.dataZoom.start = 0;
                   batteryOption.dataZoom.start = 0;
               }
               $.each(res.data, function(i, item){
                   date.push(item.create_time);
                   fillLevel.push(item.occupancy);
                   batteryLevel.push(item.electric_level);
                   temperature.push(item.temperature);
               });
               //var fillChart = echarts.init(document.getElementById('chart'));

        // 使用刚指定的配置项和数据显示图表。
        fillChart.setOption(option);
        temperatureChart.setOption(temperatureOption);
        batteryChart.setOption(batteryOption);
               }
          }
    });


    var oTable = $('#data-table').dataTable({
                "aLengthMenu": [
                    [5, 15, 20, -1],
                    [5, 15, 20, "All"] // change per page values here
                ],
        // set the initial value
                "iDisplayLength": 15,
        "sDom": "<'row'<'col-lg-6'l><'col-lg-6'f>r>t<'row'<'col-lg-6'i><'col-lg-6'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
                    "sLengthMenu": "_MENU_ records per page",
                    "oPaginate": {
                        "sPrevious": "Prev",
                        "sNext": "Next"
                    }
                },
        "aoColumnDefs": [{
                'bSortable': false,
                'aTargets': [0]
            }
        ],
        "aaSorting": [[ 0, "desc" ]]
    });

            jQuery('#data-table_wrapper .dataTables_filter input').addClass("form-control medium"); // modify table search input
            jQuery('#data-table_wrapper .dataTables_length select').addClass("form-control xsmall"); // modify table per page dropdown
});
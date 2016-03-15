/**
 * Created by qitian on 2016/2/1.
 */
$(document).ready(function(){
    namespace = '/device';
    var myChart = echarts.init(document.getElementById('chart'));
    var date = [];
    var data = [];

    var option = {
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
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // use mac for eventName
    var eventName = $('#device-mac').text().replace(/[ ]/g,"");
    //
    socket.on(eventName, function(msg) {
        var electric_level = '--';
        if (msg.electric_level >= 7) {
            var electric_level = '100 %'
        }else {
            electric_level = msg.electric_level * 15 + ' %'
        }
        $('#device-data').prepend("<tr>" +
            "<td>" + msg.create_time + "</td>" +
            "<td>" + msg.occupancy + " %</td>" +
            "<td>" + msg.temperature + " ℃</td>" +
            "<td>" + msg.electric_level + "</td></tr>");

        date.push(msg.create_time);
        data.push(msg.occupancy);
        myChart.setOption(option);
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
               $.each(res.data, function(i, item){
                   date.push(item.create_time);
                   data.push(item.occupancy);
               });
               //var myChart = echarts.init(document.getElementById('chart'));

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
               }
          }
    });
});
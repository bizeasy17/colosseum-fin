// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';




/* Notifications JS basic client */
$(function () {
    $('#id_stock_name').blur(function(){
        // if(validateStockName()){
        // }
        $('#id_stock_code').val('000001');
    });

    function number_format(number, decimals, dec_point, thousands_sep) {
        // *     example: number_format(1234.56, 2, ',', ' ');
        // *     return: '1 234,56'
        number = (number + '').replace(',', '').replace(' ', '');
        var n = !isFinite(+number) ? 0 : +number,
            prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
            sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
            dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
            s = '',
            toFixedFix = function(n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
            };
        // Fix for IE parseFloat(0.55).toFixed(0) = 0;
        s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
        if (s[0].length > 3) {
            s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
        }
        if ((s[1] || '').length < prec) {
            s[1] = s[1] || '';
            s[1] += new Array(prec - s[1].length + 1).join('0');
        }
        return s.join(dec);
    }

    // Bar Chart Example
    // function draw_sample_charts(){
    //     var endpoint = "/report/data/sample/";
        
    //     var ctx = document.getElementById("myBarChart");
    //     var rptData;
    //     $.ajax({
    //         url: endpoint,
    //         success: function(data ){
    //             // rptData = data;
                
    //             var myBarChart = new Chart(ctx, {
    //                 type: 'bar',
    //                 data: {
    //                     labels: ["January", "February", "March", "April", "May", "June"],
    //                     datasets: [{
    //                     label: "Revenue",
    //                     backgroundColor: "#4e73df",
    //                     hoverBackgroundColor: "#2e59d9",
    //                     borderColor: "#4e73df",
    //                     data: data,
    //                     }],
    //                 },
    //                 options: {
    //                     maintainAspectRatio: false,
    //                     layout: {
    //                     padding: {
    //                         left: 10,
    //                         right: 25,
    //                         top: 25,
    //                         bottom: 0
    //                     }
    //                     },
    //                     scales: {
    //                     xAxes: [{
    //                         time: {
    //                         unit: 'month'
    //                         },
    //                         gridLines: {
    //                         display: false,
    //                         drawBorder: false
    //                         },
    //                         ticks: {
    //                         maxTicksLimit: 6
    //                         },
    //                         maxBarThickness: 25,
    //                     }],
    //                     yAxes: [{
    //                         ticks: {
    //                         min: 0,
    //                         max: 15000,
    //                         maxTicksLimit: 5,
    //                         padding: 10,
    //                         // Include a dollar sign in the ticks
    //                         callback: function(value, index, values) {
    //                             return '$' + number_format(value);
    //                         }
    //                         },
    //                         gridLines: {
    //                         color: "rgb(234, 236, 244)",
    //                         zeroLineColor: "rgb(234, 236, 244)",
    //                         drawBorder: false,
    //                         borderDash: [2],
    //                         zeroLineBorderDash: [2]
    //                         }
    //                     }],
    //                     },
    //                     legend: {
    //                     display: false
    //                     },
    //                     tooltips: {
    //                     titleMarginBottom: 10,
    //                     titleFontColor: '#6e707e',
    //                     titleFontSize: 14,
    //                     backgroundColor: "rgb(255,255,255)",
    //                     bodyFontColor: "#858796",
    //                     borderColor: '#dddfeb',
    //                     borderWidth: 1,
    //                     xPadding: 15,
    //                     yPadding: 15,
    //                     displayColors: false,
    //                     caretPadding: 10,
    //                     callbacks: {
    //                         label: function(tooltipItem, chart) {
    //                         var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
    //                         return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
    //                         }
    //                     }
    //                     },
    //                 }
    //             });
    //         },
    //     });
    // }

    var barCount = 60;
    var initialDateStr = '20200110';
    var ctx1 = document.getElementById('myStockChart').getContext('2d');

    // Bar Chart Example
    var klineEndpoint = 'endpoint/stock_kline/000001.SZ/20191201/20191231';

    $.ajax({
        url: klineEndpoint,
        success: function(data){
            // ctx1.canvas.width = 1000;
            // ctx1.canvas.height = 250;
            var chart = new Chart(ctx1, {
                type: 'candlestick',
                data: {
                    datasets: [{
                        label: 'CHRT - Chart.js Corporation',
                        data: getRandomData(initialDateStr, barCount)
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            afterBuildTicks: function(scale, ticks) {
                                var majorUnit = scale._majorUnit;
                                var firstTick = ticks[0];
                                var i, ilen, val, tick, currMajor, lastMajor;

                                val = luxon.DateTime.fromMillis(ticks[0].value);
                                if ((majorUnit === 'minute' && val.second === 0)
                                        || (majorUnit === 'hour' && val.minute === 0)
                                        || (majorUnit === 'day' && val.hour === 9)
                                        || (majorUnit === 'month' && val.day <= 3 && val.weekday === 1)
                                        || (majorUnit === 'year' && val.month === 0)) {
                                    firstTick.major = true;
                                } else {
                                    firstTick.major = false;
                                }
                                lastMajor = val.get(majorUnit);

                                for (i = 1, ilen = ticks.length; i < ilen; i++) {
                                    tick = ticks[i];
                                    val = luxon.DateTime.fromMillis(tick.value);
                                    currMajor = val.get(majorUnit);
                                    tick.major = currMajor !== lastMajor;
                                    lastMajor = currMajor;
                                }
                                return ticks;
                            }
                        }]
                    }
                }
            });
        }
    });

    var getRandomInt = function(max) {
        return Math.floor(Math.random() * Math.floor(max));
    };

    function randomNumber(min, max) {
        return Math.random() * (max - min) + min;
    }

    function randomBar(date, lastClose) {
        var open = randomNumber(lastClose * 0.95, lastClose * 1.05).toFixed(2);
        var close = randomNumber(open * 0.95, open * 1.05).toFixed(2);
        var high = randomNumber(Math.max(open, close), Math.max(open, close) * 1.1).toFixed(2);
        var low = randomNumber(Math.min(open, close) * 0.9, Math.min(open, close)).toFixed(2);
        return {
            t: date.valueOf(),
            o: open,
            h: high,
            l: low,
            c: close
        };

    }

    function getRandomData(dateStr, count) {
        var date = luxon.DateTime.fromRFC2822(dateStr);
        var data = [randomBar(date, 30)];
        while (data.length < count) {
            date = date.plus({days: 1});
            if (date.weekday <= 5) {
                data.push(randomBar(date, data[data.length - 1].c));
            }
        }
        return data;
    }

    var update = function() {
        var dataset = chart.config.data.datasets[0];

        // candlestick vs ohlc
        var type = document.getElementById('type').value;
        dataset.type = type;

        // color
        var colorScheme = document.getElementById('color-scheme').value;
        if (colorScheme === 'neon') {
            dataset.color = {
                up: '#01ff01',
                down: '#fe0000',
                unchanged: '#999',
            };
        } else {
            delete dataset.color;
        }

        // border
        var border = document.getElementById('border').value;
        var defaultOpts = Chart.defaults.global.elements[type];
        if (border === 'true') {
            dataset.borderColor = defaultOpts.borderColor;
        } else {
            dataset.borderColor = {
                up: defaultOpts.color.up,
                down: defaultOpts.color.down,
                unchanged: defaultOpts.color.up
            };
        }

        chart.update();
    };

    document.getElementById('update').addEventListener('click', update);

    document.getElementById('randomizeData').addEventListener('click', function() {
        chart.data.datasets.forEach(function(dataset) {
            dataset.data = getRandomData(initialDateStr, barCount + getRandomInt(10));
        });
        update();
    });
});
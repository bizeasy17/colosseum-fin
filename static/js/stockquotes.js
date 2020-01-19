// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

/* Notifications JS basic client */
$(function () {
    var klineBaseEndpoint = 'endpoint/stock_kline/';
    var realtimeQuoteBaseEndpoint = 'endpoint/realtime-quotes/';
    var stockCodeBaseEndpoint = 'endpoint/stockcode/';
    var stockNameBaseEndpoint = 'endpoint/stockname/';
    var chartCanvas = document.getElementById('myStockChart').getContext('2d');

    // when lost focus get the code auto filled
    $('#id_stock_name').blur(function(){
        // if(validateStockName()){
        // }
        // $('#id_stock_code').val('000001');
        // mock for now
        var stockName = document.getElementById('id_stock_name').value;
        var stockCode = '000001.SZ'; //getStockcodeByName(stockName);
        var startDate = '20191201';
        var endDate = '20191231';
        // showStockKline(stockName, stockCode, startDate, endDate);
        showStockKlineByName(stockName, startDate, endDate)
    });

    // when lost focus get the code auto filled
    $('#id_stock_code').blur(function(){
        // if(validateStockName()){
        // }
        // $('#id_stock_code').val('000001');
        // mock for now
        var stockCode = document.getElementById('id_stock_code').value;
        var startDate = '20191201';
        var endDate = '20191231'
        
        showStockKlineByCode(stockCode, startDate, endDate);
    });

    function getStockcodeByName1(callback){
        var stockCode;
        var stockCodeEndpoint = stockCodeBaseEndpoint + arguments[1];
        $.ajax({
            url: stockCodeEndpoint,
            success: function(data){
                stockCode = data;
                callback(arguments[1], arguments[2], arguments[3], stockCode);
            }
        });
    }

    function getStockcodeByName(stockName){
        var stockCode;
        var stockCodeEndpoint = stockCodeBaseEndpoint + stockName;
        $.ajax({
            url: stockCodeEndpoint,
            success: function(data){
                stockCode = data;
                return stockCode;
            }
        });
    }

    function getStocknameByCode(stockCode){
        var stockName;
        var stockNameEndpoint = stockNameBaseEndpoint + stockCode;
        $.ajax({
            url: stockNameEndpoint,
            success: function(data){
                stockName = data;
                return stockName;
            }
        });
    }

    // var barCount = 60;
    // var initialDateStr = '20200110';
    function showStockKlineByName(stockName, startDate, endDate){
        // Bar Chart Example
        var stockCodeEndpoint = stockCodeBaseEndpoint + stockName;
        $.ajax({
            url: stockCodeEndpoint,
            success: function(data){
                stockCode = data;
                var klineEndpoint = klineBaseEndpoint + stockCode + '/' + startDate + '/' + endDate;
                chartRender(klineEndpoint, stockName, stockCode);  
            }
        });
    }

    function showStockKlineByCode(stockCode, startDate, endDate){
        // Bar Chart Example
        var klineEndpoint = klineBaseEndpoint + stockCode + '/' + startDate + '/' + endDate;
        chartRender(klineEndpoint, '', stockCode);
    }

    function chartRender(klineEndpoint, stockName, stockCode){
        $.ajax({
            url: klineEndpoint,
            success: function(data){
                var chart = new Chart(chartCanvas, {
                    type: 'candlestick',
                    data: {
                        datasets: [{
                            label: stockCode + ' - ' + stockName,
                            data: data,
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
    }

    function showStockRealtimeQuote(stockCode, canvasId){
        var chartCanvas = document.getElementById(canvasId).getContext('2d');
        // Bar Chart Example
        
    }
    
});
window.onload = function() {
    var dataPoints = [];
    var chart;
    $.getJSON("https://canvasjs.com/services/data/datapoints.php?xstart=1&ystart=25&length=20&type=json&callback=?", function(data) {
        $.each(data, function(key, value){
            dataPoints.push({x: value[0], y: parseInt(value[1])});
        });
        chart = new CanvasJS.Chart("chartContainer",{
            title:{
                text:"Usage Vs Cost"
            },
            data: [{
                type: "line",
                dataPoints : dataPoints,
            }]
        });
        chart.render();
        updateChart();
    });
    function updateChart() {
        $.getJSON("https://canvasjs.com/services/data/datapoints.php?xstart=" + (dataPoints.length + 1) + "&ystart=" + (dataPoints[dataPoints.length - 1].y) + "&length=1&type=json&callback=?", function(data) {
            $.each(data, function(key, value) {
                dataPoints.push({
                    x: parseInt(value[0]),
                    y: parseInt(value[1])
                });
            });
            chart.render();
            setTimeout(function(){updateChart()}, 1000);
        });
    }
}

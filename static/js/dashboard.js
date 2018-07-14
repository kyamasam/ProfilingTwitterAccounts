(function($) {
  'use strict';
  $(function() {
    if ($("#earning-chart").length) {
      Chart.defaults.global.legend.labels.usePointStyle = true;
      var ctx = document.getElementById('earning-chart').getContext("2d");

      var gradientStrokeLine = ctx.createLinearGradient(500, 0, 100, 0);
      gradientStrokeLine.addColorStop(0, 'rgba(0, 133, 255, .7)');
      gradientStrokeLine.addColorStop(1, 'rgba(53,35,192,.5)');

      var gradientStrokeFill = ctx.createLinearGradient(500, 0, 100, 0);
      gradientStrokeFill.addColorStop(0, 'rgba(0, 133, 255, .2)');
      gradientStrokeFill.addColorStop(1, 'rgba(53,35,192,.2)');

      var earningChartData = {
        datasets: [{
          label: "Negative",
            borderColor: '#ed7879',
            fill: true,
            backgroundColor: '',
            borderWidth: 4,
            data: [30, 50, 30, 50, 40, 85, 60]
        },
          {
          label: "Positive",
            borderColor: '#66d1ad',
            fill: true,
            backgroundColor: '',
            borderWidth: 4,
            data: [25, 53, 10, 20, 30, 175, 30]
        }
        ],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL"]
      };
      var earningChartOptions = {
        responsive: true,
        animation: {
          animateScale: true,
          animateRotate: true
        },
        legend: false,
        elements: { 
          point: { 
            radius: 0 
          } 
        },
        scales: {
          xAxes: [{
            gridLines: {
              color: 'rgba(0, 0, 0, .02)'
            },
          }],
          yAxes: [{
            gridLines: {
              color: 'rgba(255, 255, 255, 0)'             
            }
          }]
        }
      };
      var earningChartCanvas = $("#earning-chart").get(0).getContext("2d");
      var earningChart = new Chart(earningChartCanvas, {
        type: 'line',
        data: earningChartData,
        options:{
          earningChartOptions,
            tooltips:{
              display:true,
        }
        }
      });
    }
  });


  var doughnutPieData = {
    datasets: [{
      data: [12, 9],
      backgroundColor: [
        '#ed7879',
        '#53c4fb',
      ],
      borderColor: [

      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'Negative',
      'Positive',
    ]
  };
  var doughnutPieOptions = {
    responsive: true,
    animation: {
      animateScale: true,
      animateRotate: true
    }
  };
if ($("#sentiment_chart").length) {
  var sentiment_chartCanvas = $("#sentiment_chart").get(0).getContext("2d");
  var sentiment_chart = new Chart(sentiment_chartCanvas, {
    type: 'doughnut',
    data: doughnutPieData,
    options: doughnutPieOptions
  });
}
})(jQuery);
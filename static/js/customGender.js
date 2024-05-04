document.addEventListener("DOMContentLoaded", function(event) {
    var chartElement = document.querySelector("#gender_pie_chart");
    var totalMale = parseInt(chartElement.dataset.totalMale);
    var totalFemale = parseInt(chartElement.dataset.totalFemale);
    var total = totalMale + totalFemale;
    var malePercentage = (totalMale / total) * 100;
    var femalePercentage = (totalFemale / total) * 100;
    
    var options = {
        series: [totalMale, totalFemale],
        labels: ['Male', 'Female'],
        chart: {
            type: 'donut',
            height: 250,
            width: 400 
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '65%'
                }
            }
        },
        dataLabels: {
            enabled: true
        },
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 200
                },
                legend: {
                    position: 'bottom'
                }
            }
        }]
    };

    var chart = new ApexCharts(document.querySelector("#gender_pie_chart"), options);
    chart.render();
});

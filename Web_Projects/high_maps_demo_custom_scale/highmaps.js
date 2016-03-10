$(function () {

    // Prepare demo data
    var data = [
        {
            "hc-key": "us-ma",
            "value": 0.007
        },
        {
            "hc-key": "us-wa",
            "value": 0.0087
        },
        {
            "hc-key": "us-ca",
            "value": 455
        },
        {
            "hc-key": "us-or",
            "value": 0.0067
        },
        {
            "hc-key": "us-wi",
            "value": 0.0025
        },
        {
            "hc-key": "us-me",
            "value": 0.0124
        },
        {
            "hc-key": "us-mi",
            "value": 0.0051
        },
        {
            "hc-key": "us-nv",
            "value": 450
        },
        {
            "hc-key": "us-nm",
            "value": 0.017
        },
        {
            "hc-key": "us-co",
            "value": 0.0032
        },
        {
            "hc-key": "us-wy",
            "value": 0.00 //data not available, defaulted to 0
        },
        {
            "hc-key": "us-ks",
            "value": 0.003
        },
        {
            "hc-key": "us-ne",
            "value": 0.0124
        },
        {
            "hc-key": "us-ok",
            "value": 0.0208
        },
        {
            "hc-key": "us-mo",
            "value": 0.0042
        },
        {
            "hc-key": "us-il",
            "value": 0.0139
        },
        {
            "hc-key": "us-in",
            "value": 0.0047
        },
        {
            "hc-key": "us-vt",
            "value": 0.0055
        },
        {
            "hc-key": "us-ar",
            "value": 0.0075
        },
        {
            "hc-key": "us-tx",
            "value": 0.0052
        },
        {
            "hc-key": "us-ri",
            "value": 0.0075
        },
        {
            "hc-key": "us-al",
            "value": 0.017
        },
        {
            "hc-key": "us-ms",
            "value": 0.01
        },
        {
            "hc-key": "us-nc",
            "value": 0.0099
        },
        {
            "hc-key": "us-va",
            "value": 0.0151
        },
        {
            "hc-key": "us-ia",
            "value": 0.0175
        },
        {
            "hc-key": "us-md",
            "value": 0.004
        },
        {
            "hc-key": "us-de",
            "value": 0.0097
        },
        {
            "hc-key": "us-pa",
            "value": 0.00 //data not available
        },
        {
            "hc-key": "us-nj",
            "value": 0.00875
        },
        {
            "hc-key": "us-ny",
            "value": 0.003
        },
        {
            "hc-key": "us-id",
            "value": 0.0045
        },
        {
            "hc-key": "us-sd",
            "value": 0.0207
        },
        {
            "hc-key": "us-ct",
            "value": 0.018
        },
        {
            "hc-key": "us-nh",
            "value": 0.00 // data not available
        },
        {
            "hc-key": "us-ky",
            "value": 0.005
        },
        {
            "hc-key": "us-oh",
            "value": 0.015
        },
        {
            "hc-key": "us-tn",
            "value": 0.0121
        },
        {
            "hc-key": "us-wv",
            "value": 0.01
        },
        {
            "hc-key": "us-dc",
            "value": 0.0045
        },
        {
            "hc-key": "us-la",
            "value": 0.0159
        },
        {
            "hc-key": "us-fl",
            "value": 0.035
        },
        {
            "hc-key": "us-ga",
            "value": 0.0151
        },
        {
            "hc-key": "us-sc",
            "value": 0.009
        },
        {
            "hc-key": "us-mn",
            "value": 0.0182
        },
        {
            "hc-key": "us-mt",
            "value": 0.0106
        },
        {
            "hc-key": "us-nd",
            "value": 0.005
        },
        {
            "hc-key": "us-az",
            "value": 460
        },
        {
            "hc-key": "us-ut",
            "value": 0.00 // data not available
        },
        {
            "hc-key": "us-hi",
            "value": 0.0212
        },
        {
            "hc-key": "us-ak",
            "value": 0.025
        },
        {
            "value": 0.00
        }
    ];

    // data.forEach(function(element){
    //     element["value"] = element["value"].toFixed(2);
    //     // element["value"] = element["value"].toFixed(2);
    // });
    

    // Initiate the chart
    $('#container').highcharts('Map', {
        chart: {
            height: 600
        },

        title : {
            text : 'Highmaps basic demo'
        },

        subtitle : {
            text : 'Source map: <a href="https://code.highcharts.com/mapdata/countries/us/us-all.js">United States of America</a>'
        },

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },

        colorAxis: {
            min: 440,
            startOnTick: true,
            endOnTick: true,
            tickInterval:5
        },

        legend:{
            enabled: true
        },

        series : [{
            data : data,
            mapData: Highcharts.maps['countries/us/us-all'],
            joinBy: 'hc-key',
            name: 'test data',
            states: {
                hover: {
                    color: '#BADA55'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            }
        }, {
            name: 'Separators',
            type: 'mapline',
            data: Highcharts.geojson(Highcharts.maps['countries/us/us-all'], 'mapline'),
            color: 'silver',
            showInLegend: false,
            enableMouseTracking: false
        }]
    });
});

// Create options for Dropdown menu
var url = "/names";
var $select = Plotly.d3.select('#selDataset');
Plotly.d3.json(url, (error, data) => {
    if (error) return console.warn(error);

    data.forEach((value, index) => {
        $select
            .append('option')
                .attr('value', value)
                    .text(value);
    });
    // default to first data set
    MetaDataSample(data[0]);
    PieChart(data[0]);
    BubbleChart(data[0]);
    GaugeChart(data[0]);
});


// Create Dynamic changes on Dropdowm button
function optionChanged(value){

    MetaDataSample(value);
    PieChart(value);
    BubbleChart(value);
    GaugeChart(value);

}

function MetaDataSample(value){
    // sample meta data
    url1 = "/metadata/";
    Plotly.d3.json(url1 + value, (error0, data0) => {
        if (error0) return console.warn(error0);
        // select id = 'sampledisplay'
        $sampleinfo = Plotly.d3.select('#sampledisplay');
        // clear the current displayed datas
        $sampleinfo.html('');
        // populate table with selected data
        Object.keys(data0).forEach((key) => {
            $sampleinfo
                .append('text').html(key + ": " + data0[key])
                .append('br');
        });
    });
}

// Create Piechart function
function PieChart(value){
    // pie chart data
    url2 = "/samples/";
    Plotly.d3.json(url2 + value, (error1, data1) => {
        if (error1) return console.warn(error1);

        Plotly.d3.json('/otu', (error2,data2) => {
          if (error2) return console.warn(error2);
            // get top ten otu_ids
          var labelid = data1.otu_ids.slice(0,10);

          var trace1 = {
            values: data1.sample_values.slice(0,10),
            labels: labelid,
            type: 'pie',
            text: labelid.map( x => data2[x]),
            textinfo: 'percent',
            hoverinfo: 'label+text+value+percent'
          };

          var plotData = [trace1];

          var layout = {
            title: value + "'s Top 10 OTU Microbiomes"
          };


          return Plotly.newPlot("piechart", plotData, layout);
        });
    });
}

function BubbleChart(value){
    // bubble chart data
    url3 = "/samples/";
    Plotly.d3.json(url3 + value, (error3, data3) => {
        if (error3) return console.warn(error3);

        Plotly.d3.json("/otu", (error4, data4) => {
          if (error4) return console.warn(error4);

          var trace1 = {
              x: data3.otu_ids,
              y: data3.sample_values,
              text: data4,
              hoverinfo: "x+y+text",
              mode: "markers",
              marker: {
                  size: data3.sample_values,
                  color: data3.otu_ids
              }
          };

          var plotData = [trace1]

          var layout = {
              title: value  + "'s Sample Volume vs OTU ID",
              showLegend: false
          }


          return Plotly.newPlot("bubblechart", plotData, layout)
        });
    });
}

function GaugeChart(value){
    //gauge chart data
    url4 = "/wfreq/";
    Plotly.d3.json(url4 + value, (error5, data5) => {
        if(error5) return console.warn(error5);

        // Enter a speed between 0 and 180
        var level = data5;

        // Trig to calc meter point
        var degrees = 180 - level*20,
             radius = .5;
        var radians = degrees * Math.PI / 180;
        var x = radius * Math.cos(radians);
        var y = radius * Math.sin(radians);

        // Path: may have to change to create a better triangle
        var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
             pathX = String(x),
             space = ' ',
             pathY = String(y),
             pathEnd = ' Z';
        var path = mainPath.concat(pathX,space,pathY,pathEnd);

        var data = [{ type: 'scatter',
           x: [0], y:[0],
            marker: {size: 28, color:'DB5F59'},
            showlegend: false,
            name: 'Washing Frequency',
            text: level,
            hoverinfo: 'text+name'},
          { values: [50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50],
          rotation: 90,
          text: ['8-9', '7-8', '6-7', '5-6', '4-5', '3-4', '2-3', '1-2', '0-1', ''],
          textinfo: 'text',
          textposition:'inside',
          marker: {colors: ['rgba(0, 112, 17, 1)', 'rgba(0, 143, 21, 1)', 'rgba(0, 179, 27, 1)',
          'rgba(0, 219, 33, 1)', 'rgba(5, 255, 43, 1)', 'rgba(66, 255, 95, 1)', 
          'rgba(97, 255, 121, 1)', 'rgba(122, 255, 142, 1)', 'rgba(173, 255, 186, 1)', 
          'rgba(255, 255, 255, 0)']},
          labels: ['8-9', '7-8', '6-7', '5-6', '4-5', '3-4', '2-3', '1-2', '0-1', ''],
          hoverinfo: 'label',
          hole: .5,
          type: 'pie',
          showlegend: false
        }];

        var layout = {
          shapes:[{
              type: 'path',
              path: path,
              fillcolor: 'DB5F59',
              line: {
                color: 'DB5F59'
              }
            }],
          title: value + ' Belly Button Weekly Washing Frequency',
          xaxis: {zeroline:false, showticklabels:false,
                     showgrid: false, range: [-1, 1]},
          yaxis: {zeroline:false, showticklabels:false,
                     showgrid: false, range: [-1, 1]}
        };


        return Plotly.newPlot('gaugechart', data, layout);
    });
}

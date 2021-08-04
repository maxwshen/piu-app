// Chart summary card

function to_dict(kvs) {
  var data = new Object();
  keys = kvs[0];
  values = kvs[1];
  for (let i = 0; i < keys.length; i++) {
    data[keys[i]] = values[i];
  }
  return data;
}

function draw_card(canvas, py_data) {
  // Load python data into dict
  info = to_dict(py_data[0]);
  card = to_dict(py_data[1]);
  details = to_dict(py_data[2]);

  // nps
  var trace1 = {
    x: card['nps'][0],
    y: card['nps'][1],
    yaxis: 'y1',
    type: 'scatter',
    mode: 'markers',
    marker: {
      color: card['nps'][1],
    },
    hoverinfo: 'x+y',
    fill: 'tozeroy',
    // fillcolor: '#ddd',
  };
  
  // timelines
  var plot_data = [trace1];
  var colors = ['#7cb82f', '#ed7495', '#00aeb3', '#8c68cb', '#f47b16'];
  for (let i = 0; i < card['timelines'].length; i++) {
    var trace = {
      x: card['timelines'][i][0],
      y: card['timelines'][i][1],
      yaxis: 'y'.concat('', (i+2).toString()),
      type: 'scatter',
      mode: 'markers',
      hoverinfo: 'x',
      marker: {
        symbol: 'square',
        size: 5,
        color: colors[i],
      }
    }
    plot_data.push(trace);
  }

  // grid subplot allocation
  var num_timelines = 5;
  var per_timeline = 0.11;
  var margin = 0.02;
  var domains = [[num_timelines*per_timeline+margin, 1]];
  for (let i = 0; i < num_timelines; i++) {
    prev_start = domains[domains.length-1][0] - margin;
    start = prev_start - per_timeline;
    domains.push([start + margin, start + per_timeline - margin]);
  }
  
  var layout = {
    grid: {
      rows: 6,
      columns: 1,
      pattern: 'coupled',
    },
    yaxis: {
      title: {text: 'Notes/second', font: {size: 12}},
      domain: domains[0], 
      fixedrange: true,
      ticklabelposition: 'inside bottom',
      hoverformat: '.1f',
    },
    yaxis2: {domain: domains[1], showgrid: false, fixedrange: true, ticklabelposition: 'inside'},
    yaxis3: {domain: domains[2], showgrid: false, fixedrange: true, ticklabelposition: 'inside'},
    yaxis4: {domain: domains[3], showgrid: false, fixedrange: true, ticklabelposition: 'inside'},
    yaxis5: {domain: domains[4], showgrid: false, fixedrange: true, ticklabelposition: 'inside'},
    yaxis6: {domain: domains[5], showgrid: false, fixedrange: true, ticklabelposition: 'inside'},

    showlegend: false,
    margin: { t: 0, r: 20, l: 20, b: 40},

    hovermode: 'x',
    xaxis: {
      fixedrange: true, hoverformat: '.1f',
      showspikes: true,
      spikesnap: 'cursor',
      spikedash: 'dot',
      spikemode: 'across+toaxis',
      spikecolor: 'black',
      spikethickness: 1,
      showgrid: true,
      gridwidth: 1,
      gridcolor: '#888',
      tickmode: 'array',
      tickvals: card['xticks'],
      ticktext: card['xlabels'],
    },
  };
  var config = {
    responsive: true,
    displayModeBar: false,
    scrollZoom: false,
  };

	Plotly.newPlot(canvas, plot_data, layout, config);
}
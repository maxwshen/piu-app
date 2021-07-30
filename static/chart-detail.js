// Chart detail

// Parsing
function to_dict(kvs) {
  var data = new Object();
  keys = kvs[0];
  values = kvs[1];
  for (let i = 0; i < keys.length; i++) {
    data[keys[i]] = values[i];
  }
  return data;
}


function parse_arrows(details) {
  var arrow_xs = [];
  var arrow_ys = [];
  var arrow_texts = [];
  for (let i = 0; i < details['arrows'].length; i++) {
    arrow_xs.push(details['arrows'][i][0]);
    arrow_ys.push(details['arrows'][i][1]);
    arrow_texts.push(details['arrows'][i][2]);
  }
  return [arrow_xs, arrow_ys, arrow_texts];
}


function get_arrow_markers(arrow_xs) {
  var markers = [];
  var mapper = {
    0: 'triangle-sw', 1: 'triangle-nw', 2: 'octagon', 
    3: 'triangle-ne', 4: 'triangle-se', 5: 'triangle-sw', 
    6: 'triangle-nw', 7: 'octagon', 8: 'triangle-ne', 9: 'triangle-se',
  };
  for (let i = 0; i < arrow_xs.length; i++) {
    markers.push(mapper[arrow_xs[i]]);
  }
  return markers;
}


// Colors
function get_arrow_colors_standard(arrow_xs) {
  var colors = [];
  var blue = '#00a0dc';
  var red = '#ec4339';
  var yellow = '#efb920';
  var mapper = {
    0: blue, 1: red, 2: yellow, 3: red, 4: blue,
    5: blue, 6: red, 7: yellow, 8: red, 9: blue,
  };
  for (let i = 0; i < arrow_xs.length; i++) {
    colors.push(mapper[arrow_xs[i]]);
  }
  return colors;
}


function get_arrow_colors_hints(arrow_texts) {
  var colors = [];
  var mapper = {
    'LT': '#f59890',
    'LH': '#c11f1d',
    'RT': '#68c7ec',
    'RH': '#0077b5',
    'HANDS': '#595c5f',
  }
  for (let i = 0; i < arrow_texts.length; i++) {
    colors.push(mapper[arrow_texts[i]]);
  }
  return colors;
}


// Drawing
function draw_holds(holds) {
  var shapes = [];
  for (let i = 0; i < holds.length; i++) {
    shape = draw_single_hold(holds[i]);
    shapes.push(shape);
  }
  return shapes;
}


function draw_single_hold(hold) {
  [x, y_start, y_end, hold_text] = hold;
  color_list = get_arrow_colors_hints([hold_text]);
  width = 0.4;
  return {
    type: 'rect',
    x0: x - width/2,
    y0: y_start,
    x1: x + width/2,
    y1: y_end,
    fillcolor: color_list[0],
    opacity: 0.5,
    line: {
        width: 0
    }
  };
}


function get_annotations(details){
  annot_x = 1;
  [line_annot_times, line_annot_texts] = details['annots'];
  var annots = [];
  for (i = 0; i < line_annot_times.length; i++) {
    single_annot = {
      x: annot_x,
      y: line_annot_times[i],
      text: line_annot_texts[i],
      xref: 'paper',
      xanchor: 'left',
      showarrow: false,
    };
    annots.push(single_annot);
  }
  return annots;
}


// Primary artist
function draw_detail(canvas, section_num, py_data) {
  info = to_dict(py_data[0]);
  card = to_dict(py_data[1]);
  details = to_dict(py_data[2][section_num-1]);

  [arrow_xs, arrow_ys, arrow_texts] = parse_arrows(details);

  var trace1 = {
    x: arrow_xs,
    y: arrow_ys,
    mode: 'markers+text',
    type: 'scattergl',
    text: arrow_texts,
    textposition: 'middle center',
    hoverinfo: 'y',
    marker: {
      symbol: get_arrow_markers(arrow_xs),
      size: 25,
      opacity: 0.5,
      // color: get_arrow_colors_standard(arrow_xs),
      color: get_arrow_colors_hints(arrow_texts),
    },
  };
  var plot_data = [trace1];

  drawn_shapes = draw_holds(details['holds']);

  var layout = {
    shapes: drawn_shapes,
    annotations: get_annotations(details),

    autosize: false,
    width: 100 + info['num_panels']*40,
    height: details['num_lines']*25,
    margin: {
      l: 60,
      r: 110,
      b: 0,
      t: 0,
    },

    title: {text: details['section_num']},

    yaxis: {fixedrange: true,
      // autorange: 'reversed',
      range: [details['plot_start_time'], details['plot_end_time']],
      tickmode: 'array',
      tickvals: details['times'],
      ticktext: details['time_labels'],
      ticklabelposition: 'outside top',
      title: {text: 'Time (seconds)', font: {size: 12}},
      showspikes: true,
      spikedash: 'dot',
      spikemode: 'across+toaxis',
      spikethickness: 1,
      spikecolor: 'black',
      spikesnap: 'cursor',
    },
    xaxis: {fixedrange: true,
      tickmode: 'array',
      tickvals: [...Array(details['num_panels']).keys()],
      ticktext: Array(details['num_panels']).fill(''),
      range: [0 - 0.25, details['num_panels'] - 1 + 0.25],
      zeroline: false,
    },
  };
  var config = {
    responsive: true,
    displayModeBar: false,
    scrollZoom: false,
  };
  Plotly.newPlot(canvas, plot_data, layout, config);
}


function assignOptions(arr, selector) {
  for (var i = 0; i < arr.length;  i++) {
    var currentOption = document.createElement('option');
    currentOption.text = arr[i];
    selector.appendChild(currentOption);
  }
}


// Primary - handle interactivity
function draw_detail_interactive(py_data) {
  var innerContainer = document.querySelector('[data-num="0"'),
  plotdiv = innerContainer.querySelector('.canvas_detail'),
  dropdown = innerContainer.querySelector('.section_selector');

  info = to_dict(py_data[0]);

  // initial choice
  draw_detail(plotdiv, 1, py_data);

  var options = Array.from({length: info['num_chart_sections']}, (_, i) => i + 1);
  assignOptions(options, dropdown);

  function updatePlot(){
    draw_detail(plotdiv, dropdown.value, py_data);
  }
    
  dropdown.addEventListener('change', updatePlot, false);
}
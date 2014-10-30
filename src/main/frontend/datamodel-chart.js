google.load('visualization', '1.1', {packages:['wordtree']});
//TODO: Wrap this functionality as an object
var tbl;
var chart;
function dataModelBegin() {
    //Initialize tbl (internal data table drawn on the chart) and chart
    tbl = new google.visualization.DataTable();
    tbl.addColumn('string', 'Phrases');
    chart = new google.visualization.WordTree(document.getElementById('chartPanel'));
}
function dataModelEnd() {
    chart.draw(tbl, 
            { height : 1000,
              width : 1000,
              wordtree: {
                format: 'implicit',
                word : 'x'
                        }
            });
}
function dataModelData( values ) {
  var p = values.p.split('/').pop();
  var y;
  if (values.y.indexOf('/') > -1) {
    y = values.y.split('/').pop();
  } else {
    y = 'data';
  };
  var text = 'x ' + p + ' ' + y
  console.log(text);
  tbl.addRow(
    [ text
    ]);
}

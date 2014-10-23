google.load('visualization', '1', {packages:['orgchart']});
//TODO: Wrap this functionality as an object
var tbl;
var chart;
var clickHandler = function( id ){};//Dummy click-handler
function initChart() {
    //Initialize tbl (internal data table drawn on the chart) and chart
    tbl = new google.visualization.DataTable();
    tbl.addColumn('string', 'UrlAndLabel');
    tbl.addColumn('string', 'ParentUrl');
    tbl.addColumn('string', 'ToolTip');//Not used but specified by orgchart
    chart = new google.visualization.OrgChart(document.getElementById('chart_panel'));//TODO: replace chart_panel by parameter
    //Get a call to selectHandler() when chart is clicked
    google.visualization.events.addListener(chart, 'select', selectHandler);
}
function setClickHandler( callback ){
  clickHandler = callback;
}
function selectHandler() {
  var rowIndex = chart.getSelection()[0].row;//This may work badly if more than one node is selected
  var rowId = tbl.getValue(rowIndex, 0);
  clickHandler( rowId );
}
function updateChart() {
    chart.draw(tbl, {allowHtml:true});
}
function addNodeToChartIfNotThere( id, label, parentId, relation) {
  if ($.inArray( id, tbl.getDistinctValues(0)) === -1) {
    addNodeToChart( id, label, parentId, relation);
  }
}
function addNodeToChart( id, label, parentId, relation) {
  tbl.addRow(
    [ { v: id, //v is the URL that child nodes can point to
        f: '<p style="font: xx-small italic;">' + relation + '</p><p>' + label + '</p>'},
        parentId,
        ""//No tooltip
    ]);
}
function removeAllNodesFromChart() {
  tbl.removeRows(0, tbl.getNumberOfRows());
}

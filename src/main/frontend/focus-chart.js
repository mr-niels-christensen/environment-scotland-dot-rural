//Make jquery Deferred objects for all the events we need to wait for: Loading Google Charts, initializing chart, document.ready
var _chartload_deferred = new $.Deferred();
google.load('visualization', '1', {packages:['orgchart'], 'callback': _chartload_deferred.resolve});
var _chart_ready_deferred = _chartload_deferred.then(function() {
  _initChart();
});
var _doc_ready_deferred = new $.Deferred();
$( document ).ready( function() {
  _doc_ready_deferred.resolve();
});

//Bind AJAX data load to hashchange event
$(window).bind( 'hashchange', function( event ) {
  _updateChartFromHashchangeEvent( event );
});

function _updateChartFromHashchangeEvent(event) {
    var iri = event.getState( 'iri' );
    sparql_predefined(
        "/sparql-queries/focus-chart.sparql.txt", 
        {'focus' : iri}, 
        _docReady_updateChartFromJson);
}

function _docReady_updateChartFromJson(response) {
  $.when(_chart_ready_deferred, _doc_ready_deferred).done(function() {
    _updateChartFromJson(response)
  });
}
  
function _updateChartFromJson(response) {
    $.each(response.results.bindings, function(index, binding){
      values = _valuesOfSparqlBinding(binding);
      //Add owned always
      _addNodeToChart(values.owned, values.ownedlabel, values.owner, 'owns');
      //Add owner if not there
      _addNodeToChartIfNotThere(values.owner, values.ownerlabel, '', '');
    });
    _updateChart();        
}

//TODO: Wrap this functionality as an object http://www.phpied.com/3-ways-to-define-a-javascript-class/
var _tbl;
var _chart;
function _initChart() {
    //Initialize _tbl (internal data table drawn on the chart) and _chart
    _tbl = new google.visualization.DataTable();
    _tbl.addColumn('string', 'UrlAndLabel');
    _tbl.addColumn('string', 'ParentUrl');
    _tbl.addColumn('string', 'ToolTip');//Not used but specified by orgchart
    _chart = new google.visualization.OrgChart(document.getElementById('chartPanel'));//TODO: replace chart_panel by parameter
    //Get a call to selectHandler() when chart is clicked
    google.visualization.events.addListener(_chart, 'select', function () {
      var rowIndex = _chart.getSelection()[0].row;//This may work badly if more than one node is selected
      var rowId = _tbl.getValue(rowIndex, 0);
      _removeAllNodesFromChart();
      _updateChart();        
      jQuery.bbq.pushState({'iri' : rowId});
    });
}

function _updateChart() {
    _chart.draw(_tbl, {allowHtml:true, size:'large'});
}
function _addNodeToChartIfNotThere( id, label, parentId, relation) {
  if ($.inArray( id, _tbl.getDistinctValues(0)) === -1) {
    _addNodeToChart( id, label, parentId, relation);
  }
}
function _addNodeToChart( id, label, parentId, _relation) {
  _tbl.addRow(
    [ { v: id, //v is the URL that child nodes can point to
        f: '<p>' + label + '</p>'},
        parentId,
        ""//No tooltip
    ]);
}
function _removeAllNodesFromChart() {
  _tbl.removeRows(0, _tbl.getNumberOfRows());
}

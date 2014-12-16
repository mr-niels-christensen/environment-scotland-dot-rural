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
    var iriType = iri.match(/\/([^/]+)#/)[1];
    sparql_predefined(
        "/sparql-queries/focus-chart-" + iriType + ".sparql.txt", 
        {'focus' : iri}, 
        _docReady_updateChartFromJson);
}

function _docReady_updateChartFromJson(response) {
  $.when(_chart_ready_deferred, _doc_ready_deferred).done(function() {
    _updateChartFromJson(response)
  });
}
  
function _updateChartFromJson(response) {
    var parentMap = {};
    var labelMap = {}
    $.each(response.results.bindings, function(index, binding){
      if (binding.p.value == 'http://dot.rural/sepake/setlabel') {
          labelMap[binding.s.value] = binding.o.value;
      } else if (binding.p.value == 'http://dot.rural/sepake/setparent') {
          parentMap[binding.s.value] = binding.o.value;          
      } else {
          console.log('ERROR: p is ' + binding.p.value);
      }
    });
    _updateChart(parentMap, labelMap);        
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
      _tbl.removeRows(0, _tbl.getNumberOfRows());
      _chart.draw(_tbl, {allowHtml:true, size:'large'});
      jQuery.bbq.pushState({'iri' : rowId});
    });
}

function _updateChart(parentMap, labelMap) {
    _tbl.removeRows(0, _tbl.getNumberOfRows());
    $.each(labelMap, function (id, label){
        _tbl.addRow(
                [ { v: id, //v is the URL that child nodes can point to
                    f: '<p>' + label + '</p>'},
                    parentMap[id],
                    ""//No tooltip
                ]);
    })
    _chart.draw(_tbl, {allowHtml:true, size:'large'});
}

google.load('visualization', '1', {packages:['orgchart']});
google.setOnLoadCallback( function() {
    $( document ).ready( function() {
        initChart();
        setClickHandler(_updateFromIri);
        $( document ).on( 'updateFromIri', _updateChartFromIri);
        _updateFromIri( "http://dot.rural/sepake/UKEOFOrganisation#Scottish%20Environment%20Protection%20Agency" );
    });
});

function _updateFromIri(iri) {
    $( document ).trigger( 'updateFromIri', iri );
  }

function _updateChartFromIri(event, iri) {
    sparql("ownerchart",
            [
            "SELECT ?owner ?ownerlabel ?owned ?ownedlabel WHERE {",
            "  {",
            "    BIND (<--IRI--> AS ?owner) .",
            "    {?owner rdfs:label ?ownerlabel} .",
            "    {?owner <owns> ?owned} .",
            "    {?owned rdfs:label ?ownedlabel} .",
            "  } UNION {",
            "    BIND (<--IRI--> AS ?focus) .",
            "    {?focus <ownedBy> ?owner} .",
            "    {?owner rdfs:label ?ownerlabel} .",
            "    {?owner <owns> ?owned} .",
            "    {?owned rdfs:label ?ownedlabel} .",
            "  }",
            "}",
            "ORDER BY ?ownerlabel ?ownedlabel",
            //TODO Add paging
           ],
           iri,
           _updateChartFromJson
    );
    removeAllNodesFromChart();
    updateChart();        
}

function _updateChartFromJson(response) {
    removeAllNodesFromChart();
    $.each(response.results.bindings, function(index, binding){
      values = _valuesOfSparqlBinding(binding);
      //Add owned always
      addNodeToChart(values.owned, values.ownedlabel, values.owner, 'owns');
      //Add owner if not there
      addNodeToChartIfNotThere(values.owner, values.ownerlabel, '', '');
    });
    updateChart();        
}

//TODO: Wrap this functionality as an object http://www.phpied.com/3-ways-to-define-a-javascript-class/
var tbl;
var chart;
var clickHandler = function( id ){};//Dummy click-handler
function initChart() {
    //Initialize tbl (internal data table drawn on the chart) and chart
    tbl = new google.visualization.DataTable();
    tbl.addColumn('string', 'UrlAndLabel');
    tbl.addColumn('string', 'ParentUrl');
    tbl.addColumn('string', 'ToolTip');//Not used but specified by orgchart
    chart = new google.visualization.OrgChart(document.getElementById('chartPanel'));//TODO: replace chart_panel by parameter
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
    chart.draw(tbl, {allowHtml:true, size:'large'});
}
function addNodeToChartIfNotThere( id, label, parentId, relation) {
  if ($.inArray( id, tbl.getDistinctValues(0)) === -1) {
    addNodeToChart( id, label, parentId, relation);
  }
}
function addNodeToChart( id, label, parentId, _relation) {
  tbl.addRow(
    [ { v: id, //v is the URL that child nodes can point to
        f: '<p>' + label + '</p>'},
        parentId,
        ""//No tooltip
    ]);
}
function removeAllNodesFromChart() {
  tbl.removeRows(0, tbl.getNumberOfRows());
}

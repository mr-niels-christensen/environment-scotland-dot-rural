google.load('visualization', '1.1', {packages:['wordtree']});
google.setOnLoadCallback( function() {
    $( document ).ready( function() {
        sparql(
                [
                 "SELECT ?rdftype (COUNT(?x) AS ?xs) (SAMPLE(?x) AS ?sample) WHERE {",
                 "    {?x rdf:type ?rdftype} .",
                 "}",
                 "GROUP BY ?rdftype",
                 "ORDER BY DESC(?xs)"
                ],
                "",
                _updateDatamodelChartFromJson
        );
    });
});

function _updateDatamodelChartFromJson(response) {
    $.each(response.results.bindings, function(index, binding){
      values = _valuesOfSparqlBinding(binding);
      $( "#chartPanel tr:last" ).after( "<tr class='rdftyperow'></tr>" );
      $( "#chartPanel tr:last" ).append( "<td>" + values.xs + "</td>" );
      $( "#chartPanel tr:last" ).append( "<td>" + values.rdftype + "</td>" );
      $( "#chartPanel tr:last" ).append( "<td class='sample'>" + values.sample + "</td>" );
    });
    $( "#chartPanel .rdftyperow" ).on( 'click', function() {
      var iri = $( this ).find( '.sample' ).text();
      _loadSample(iri);
    });
};

function _loadSample(iri) {
  sparql([
          "SELECT ?p ?y WHERE {",
          "    {<--IRI--> ?p ?y} .",
          "}",
          "ORDER BY ?p"
          ],
          iri,
          _updateSampleChartFromJson);
}

function _updateSampleChartFromJson(response) {
  $ ( "#samplePanel .datarow" ).remove();
  $.each(response.results.bindings, function(index, binding){
    values = _valuesOfSparqlBinding(binding);
    $( "#samplePanel tr:last" ).after( "<tr class='datarow'></tr>" );
    $( "#samplePanel tr:last" ).append( "<td>" + values.p + "</td>" );
    $( "#samplePanel tr:last" ).append( "<td>" + values.y + "</td>" );
  });
};

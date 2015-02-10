$( document ).ready( function() {
  $( '#sparqlForm .submitDefaultButton' ).on( 'click', function() {
    sparql("form",
        [$( '#sparqlForm #sparqlQuery' ).val()
        ],
        "",
        _updateQueryResponseFromJson
    );
  });
  $( '#sparqlForm .submitNewdataButton' ).on( 'click', function() {
    sparql_nondefault_graph(
        "newdata",
        "form",
        [$( '#sparqlForm #sparqlQuery' ).val()
        ],
        "",
        _updateQueryResponseFromJson
    );
  });
  $( '#sparqlForm .submitMetricsButton' ).on( 'click', function() {
    sparql_nondefault_graph(
        "metrics",
        "form",
        [$( '#sparqlForm #sparqlQuery' ).val()
        ],
        "",
        _updateQueryResponseFromJson
    );
  });
});

function _updateQueryResponseFromJson(response) {
    $( "#sparqlResponse .datarow" ).remove();
    $( "#sparqlResponse th" ).attr('colspan' , response.head.vars.length);
    $( "#sparqlResponse tr:last" ).after( "<tr class='datarow'></tr>" );
    for (index in response.head.vars) {
        $( "#sparqlResponse tr:last" ).append( "<th>" + response.head.vars[index] + "</th>" );
    }
    $.each(response.results.bindings, function(index, binding){
      $( "#sparqlResponse tr:last" ).after( "<tr class='datarow'></tr>" );
      for (index in response.head.vars) {
        var b = binding[response.head.vars[index]];
        var v = (b) ? b.value : '';
        $( "#sparqlResponse tr:last" ).append( "<td>" + v + "</td>" );        
      }
    });
};

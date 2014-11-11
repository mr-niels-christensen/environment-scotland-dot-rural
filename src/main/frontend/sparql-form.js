$( document ).ready( function() {
  $( '#sparqlForm .submitButton' ).on( 'click', function() {
    sparql("form",
        [$( '#sparqlForm #sparqlQuery' ).text()
        ],
        "",
        _updateQueryResponseFromJson
    );
  });
});

function _updateQueryResponseFromJson(response) {
    $( "#sparqlResponse .datarow" ).remove();
    $.each(response.results.bindings, function(index, binding){
      $( "#sparqlResponse tr:last" ).after( "<tr class='datarow'></tr>" );
      for (key in binding) {
        $( "#sparqlResponse tr:last" ).append( "<td>" + binding[key].value + "</td>" );        
      }
    });
};

$( document ).ready( function() {
  $( ".x10" ).each( function(index, dom_element) {
    var new_elems = [];
    var n_copies = 9;
    for (i = 0; i < n_copies; i++) {
      new_elems.push($(dom_element).children().clone());
    }
    for (i = 0; i < n_copies; i++) {
      $(dom_element).append(new_elems[i]);
    }
  });
  $(window).bind( 'hashchange', _updatePeopleFromIri);
});

function _updatePeopleFromIri(event) {
  var iri = event.getState( 'iri' );
  sparql("members",
          [
          "SELECT * WHERE {",
          "    BIND (<--IRI--> AS ?focus) .",
          "    {?focus prov:hadMember ?person} .",
          "    {?person foaf:givenName ?given} .",
          "    {?person foaf:familyName ?family} .",
          "    BIND (CONCAT(?given, ' ', ?family) AS ?label)",
          "}",
          "ORDER BY ASC(?family)",
          "LIMIT 11",
         ],
         iri,
         _updatePeopleFromJson
  );    
}

function _updatePeopleFromJson(response) {
    var bindings = response.results.bindings;
    $( "#personList .personWrapper" ).each( function(index, dom_elem) {//TODO: #personList -> .personList to allow several
      if (bindings.length > 0) {
        $( dom_elem ).data( bindings.shift() );
        $( dom_elem ).find( ".personLink" ).text( $( dom_elem ).data().label.value );
        $( dom_elem ).removeClass( "noData" );
      } else {
        $( dom_elem ).addClass( "noData" );                  
      }
    });
    if (bindings.length > 0) { //More results to display
      $( "#personList" ).removeClass( "noMore" );
    } else {
      $( "#personList" ).addClass( "noMore" );          
    }
}

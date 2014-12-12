sparql("suggestions",
            [
            "SELECT * WHERE {",//TODO: Get type, but only one record per id, maybe using #3
            "    {?id rdfs:label ?label} .",
            "}",
           ],
           "",
           _initSearchFromJson
);

function _initSearchFromJson(response) {
    _initSearchFromPolishedData( {items: $.map( response.results.bindings, function(binding, index) {
      return _valuesOfSparqlBinding(binding);//TODO more public naming
    })});
}

function _docReady_initSearchFromPolishedData(data) {
  $( document ).ready( function() {
    _initSearchFromPolishedData(data);
  });
}

function _initSearchFromPolishedData(data) {
  $( '#search' ).typeahead(
      {
        highlight: true,
        hint: false,
      },
      {
        name: "projects",
        source: substringMatcher(data.items),//TODO: Use Bloodhound
        displayKey: "label",
      }).on( 'typeahead:selected', function(jQueryEvent, suggestionObject, nameOfDataset) {
          var link_url = jQuery.param.fragment( '/focus.html', {'iri' : suggestionObject.id} );
          document.location.href = link_url;  
      });
  $( "#searchForm" ).submit(function( event ) {
    event.preventDefault();
    var link_url = jQuery.param.fragment( '/search.html', {'query' : $( '#search' ).val()} );
    document.location.href = link_url; 
  });
}

var substringMatcher = function(projs) {
  $.each(projs, function(i, proj) {
    proj.label = proj.label.toLowerCase();
  });
  return function findMatches(q, cb) {
    var matches, substrRegex;
 
    // an array that will be populated with substring matches
    matches = [];
 
    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');
 
    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(projs, function(i, proj) {
      if (substrRegex.test(proj.label)) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push(proj);
      }
    });
 
    cb(matches);
  };
};


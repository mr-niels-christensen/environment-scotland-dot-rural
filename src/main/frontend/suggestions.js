$( document ).ready( function() {
    sparql("suggestions",
            [
            "SELECT * WHERE {",//TODO: Get type, but only one record per id, maybe using #3
            "    {?id rdfs:label ?label} .",
            "}",
           ],
           "",
           _initSearchFromJson
    );
});

function _initSearchFromJson(response) {
    _initSearchFromPolishedData( {items: $.map( response.results.bindings, function(binding, index) {
      return _valuesOfSparqlBinding(binding);//TODO more public naming
    })});
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
          $( document ).trigger( 'updateFromIri', suggestionObject.id );
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


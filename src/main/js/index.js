function indexJsInit() {
  $('#search').one( "preloaded", initSearch);
  fuseki( "searchables", "");
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
}

function initSearch(event, data) {
  $('#search').typeahead({},
      {
        source: substringMatcher(data.items),//TODO: Use Bloodhound
        displayKey: "label",
        templates: {
          suggestion: function (proj) { return "<p class='searchsuggestion'>" + proj.label + "</p>"; },
        },
      });  
}

var substringMatcher = function(projs) {
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


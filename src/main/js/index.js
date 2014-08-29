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
      if ((substrRegex.test(proj.label)) || (substrRegex.test(proj.summary))) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push(proj);
      }
    });
 
    cb(matches);
  };
};

var projects = [{
  label: 'RURAL DIGITAL ECONOMY RESEARCH HUB', 
  summary: 'One of the three RCUK Digital Economy Research Hubs. Exploring how digital technologies can have a transformational impact on rural communities and business. User-centric activity is based around four interconnecting themes: Accessibility & Mobilities, Healthcare, Enterprise & Culture, and Natural Resource Conservation.',
}];

$('#search').typeahead({},
{
  source: substringMatcher(projects),
  displayKey: "label",
});
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

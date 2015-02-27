$(window).bind( 'hashchange', _updateFocusFromIri);

function _updateFocusFromIri(event) {
    var iri = event.getState( 'iri' );
    $( '#focusPanel' ).empty();
    sparql_predefined(
        "/sparql-queries/focus.sparql.txt", 
        {'focus' : iri}, 
        _docReady_updateFocusFromJson);    
}

function _rdfs_label(parsed) {
  return parsed['http://www.w3.org/2000/01/rdf-schema#label'][0]
}

function _first_or_undefined(parsed, iri) {
  var sent = parsed[iri];
  if (sent) {
    return sent[0];
  } else {
    return undefined;
  }  
}

function _sepake_htmlDescription(parsed) {
  return _first_or_undefined(
    parsed, 
    'http://dot.rural/sepake/htmlDescription');
}

function _prov_startedAtTime(parsed) {
  return _first_or_undefined(
    parsed,
    'http://www.w3.org/ns/prov#startedAtTime');
}

function _prov_endedAtTime(parsed) {
  return _first_or_undefined(
    parsed,
    'http://www.w3.org/ns/prov#endedAtTime');
}

function _foaf_homepage(parsed) {
  return parsed['http://xmlns.com/foaf/0.1/homepage'] || [];
}

function _dc_issued(parsed) {
  return _first_or_undefined(
    parsed,
    'http://purl.org/dc/elements/1.1/issued');
}

function _updateFocusFromJson(response) {
    try {
        var parsed = sparqlListToObject(response, "p", "y");
        $( '#focusPanel' ).append('<h2 class="focusLabel"></h2>');
        $( '#focusPanel .focusLabel' ).html(_rdfs_label(parsed));
        $( '#focusPanel' ).append('<p class="focusDescription"></p>');
        $( '#focusPanel .focusDescription' ).html(_sepake_htmlDescription(parsed) || "(No summary)");
        if (!_sepake_htmlDescription(parsed) && _focus_is_org()) {
          _set_html_from_dbpedia_description( '#focusPanel .focusDescription', _rdfs_label(parsed) );
        }
        if (_prov_startedAtTime(parsed)) {
          $( '#focusPanel' ).append('<p class="focusStart"></p>');
          $( '#focusPanel .focusStart' ).append('<strong>Started</strong>      ');
          $( '#focusPanel .focusStart' ).append(_prov_startedAtTime(parsed));
        };
        if (_prov_endedAtTime(parsed)) {
          $( '#focusPanel' ).append('<p class="focusEnd"></p>');
          $( '#focusPanel .focusEnd' ).append('<strong>Ended</strong>      ');
          $( '#focusPanel .focusEnd' ).append(_prov_endedAtTime(parsed));
        };
        if (_dc_issued(parsed)) {
          $( '#focusPanel' ).append('<p class="focusIssued"></p>');
          $( '#focusPanel .focusIssued' ).append('<strong>Published</strong>      ');
          $( '#focusPanel .focusIssued' ).append(new Date(Date.parse(_dc_issued(parsed))).toDateString());
        };
        $.each(_foaf_homepage(parsed), function(index, homepage){
          $( '#focusPanel' ).append('<p class="focusHomepage"></p>');
          $( '#focusPanel .focusHomepage:last' ).append('<strong>Homepage</strong>      ');
          $( '#focusPanel .focusHomepage:last' ).append('<a target="_blank"></a>');
          $( '#focusPanel .focusHomepage:last a' ).text(homepage);
          $( '#focusPanel .focusHomepage:last a' ).attr("href", homepage);
        });
		//metrics link
		$( '#focusPanel' ).append('<span class="metricsLink">Viewing metrics</span>');
		$( "#focusPanel .metricsLink" ).on( 'click', function() {
		  var iri = jQuery.bbq.getState('iri');
	      var link_url = jQuery.param.fragment( '/metrics.html', {'iri' : iri}  );
          document.location.href = link_url;
        });
    } catch (err) {
      console.log( err );
    }
}

function _docReady_updateFocusFromJson(response) {
  $( document ).ready( function() {
    _updateFocusFromJson(response)
  });
}

function _focus_is_org() {
  var iri = jQuery.bbq.getState('iri');
  if (iri) {
    var iriType = iri.match(/\/([^/]+)#/)[1];
    return (iriType == 'UKEOFOrganisation');
  } else {
    return false;
  };
}


function _set_html_from_dbpedia_description(selector, search_for) {
  $.ajax({
    url: "http://lookup.dbpedia.org/api/search/KeywordSearch",
    data: {
      "QueryString" : search_for,
      "MaxHits" : 1,},
    dataType: 'json',
    success: function( response ) {
      if ( response.results[0] ) {
        $( selector ).html(response.results[0].description + " <i>[Source: Wikipedia]</i>");
      };
    },
    timeout: 2500,
  });
}


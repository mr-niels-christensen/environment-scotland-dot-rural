Generate a custom report
========================

This document is a guide on how to generate custom reports on the metrics and the data in the Discover Research application.

## Execute any SPARQL query from the web interface

Go to the [data.html](http://searchtool1.appspot.com/data.html) page and locate the "SPARQL query" form. This allows you to run a query on any of the three RDF graphs used by the system. 

_Note_: The form is perfectly _safe_ to use. It is not possible to update, delete or corrupt the data. It is also not possible to overload the system, because any request will be terminated if it runs for 60 seconds (this is a unchageable policy of Google AppEngine).

For example, to get a feeling for the data in the `metrics` graph, type
```sparql
SELECT ?subj ?pred ?obj WHERE {
  ?subj ?pred ?obj .
}
LIMIT 20
```
and press "Query metrics". The table below the form will show the query result after a few seconds.

To get a report of the most viewed resources, try entering
```sparql
SELECT ?subj (COUNT(*) AS ?count) (SAMPLE(?label) AS ?title) WHERE {
  ?subj <http://dot.rural/sepake/metrics/focushit> ?obj .
  ?subj <http://www.w3.org/2000/01/rdf-schema#label> ?label .
}
GROUP BY ?subj
ORDER BY DESC(?count)
LIMIT 20
```
and press "Query default" (the `metrics` graph cannot provide the titles so you need to use the `default` graph).

## Relating the system's triples to standard ontologies

Section 2 of the file [src/main/frontend/sparql-backend/seed.sparql.txt](https://github.com/mr-niels-christensen/environment-scotland-dot-rural/blob/master/src/main/frontend/sparql-backend/seed.sparql.txt#L51) relates the predicates used with the `PROV` and `FOAF` ontologies. See also [http://www.w3.org/TR/prov-o/](http://www.w3.org/TR/prov-o/) and [http://xmlns.com/foaf/spec/](http://xmlns.com/foaf/spec/)

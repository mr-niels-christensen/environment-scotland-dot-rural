Refine Search - Adding an item
==============================

It is assumed that the item to add exists in the database.

In index.py (src\main\dotruralsepake\search) in the function `_search_documents_from_pairs` add the following line right after the statement with id_to_doc[doc_id].fields.append… for the corresponding data.
```python
id_to_doc[doc_id].facets.append(search.AtomFacet(name='<facet-name>', value=<value>))
```

Note: indexing needs to be run at this point for these changes to take effect.

In search.py (src\main\dotruralsepake\search) add the new facet name to the array at the top of the file:
```python
facetNames = ['publicationYear', ‘<facet-name>’];
```

in search-results.js (src\main\frontend) add the label for this new facet (the name that will be displayed on the page) by adding it to the array at the top of the file:
```python
var facetLabel = {'publicationYear': 'Year of publication', '<facet-name>': '<facet-label>'};
```

To learn more about Google App Engine Faceted Search: https://cloud.google.com/appengine/docs/python/search/faceted_search

### Example : integrating type

In index.py in the function `_search_documents_from_pairs`:
```python
#Add type
for (doc_id, doc) in id_to_doc.iteritems():
  type = self._graph.value(subject = doc_id, predicate = RDF.type, default = '')
  id_to_doc[doc_id].fields.append(search.TextField(name='type', value=type))
  id_to_doc[doc_id].facets.append(search.AtomFacet(name='type', value=type))
  ```
Also, add: `from rdflib import RDF`  (at the top of the file)

(indexing)

In search.py:
```python
facetNames = ['publicationYear', ‘type’];
```

in search-results.js:
```python
var facetLabel = {'publicationYear': 'Year of publication', 'type': 'Type'};
```

Note:
At this point, there is a new 'Type' item displaying in the refine search with raw types displayed.
This is clearly not a finished feature at this point. More work will be needed to display a readable type and account for conflicting types.

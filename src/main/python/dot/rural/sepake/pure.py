'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from dot.rural.sepake.sparql_utils import expand_and_parse

@expand_and_parse
def INSERT_PROJECT():
    return '''
INSERT {{
    ?projecturi <{rdf.type}> <{sepake.PureProject}>
}}
WHERE {{
    ?coreresult <http://atira.dk/schemas/pure4/model/core/stable#content> ?corecontent .
    ?corecontent <#uuid> ?uuid .
    BIND (URI(CONCAT(str(<{sepake.PureProject}>), "#", ENCODE_FOR_URI(?uuid))) AS ?projecturi)
}}
'''
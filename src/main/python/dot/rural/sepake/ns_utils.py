'''
Created on 9 Oct 2014

@author: s05nc4
'''
from rdflib import URIRef

'''Used as a marker for members that are to be treated as RDF names.'''
RDF_NAME = object()

class _URIRefCreator(type):
    '''See http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example/
       A metaclass is required in order to assign a static member of a class
       outside its definition.
       This metaclass transforms any static member that is equal to RDF_NAME
       into an rdflib.URIRef based on the static member's name.
    '''
    def __getattribute__(self, name):
        '''This method will be called when you access MYCLASS.MYSTATICMEMBER if
           MYCLASS.__metaclass__ == _URIRefCreator
        '''
        try:
            x = type.__getattribute__(self, name) #This is the default lookup operation
            if x is RDF_NAME: #Replace the dummy value with a URIRef based on name
                return URIRef(type.__getattribute__(self, 'BASE_URI') + '#' + name)
            else:
                return x
        except AttributeError:
            raise AttributeError('Attribute "%s" missing. You may want to add "%s = RDF_NAME" to your namespace class' % (name, name))
        
def namespace(base_uri):
    '''Usage: @namespace('http://example.com')
              class MyClass:
                  myRdfName = RDF_NAME
        Transforms MyClass so that MyClass.myRdfName will equal
        URIRef('http://example.com#myRdfName')
    '''
    def class_rebuilder(cls):
        class NamespaceClass(cls):
            __metaclass__ = _URIRefCreator
            BASE_URI = base_uri
        return NamespaceClass
    return class_rebuilder
        
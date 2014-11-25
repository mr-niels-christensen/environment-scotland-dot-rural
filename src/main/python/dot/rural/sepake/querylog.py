import logging
from rdflib.plugins.sparql.evaluate import evalPart
from rdflib.plugins.sparql import CUSTOM_EVALS
from time import time
from StringIO import StringIO
from appengine.ndbstore import CoarseNDBStore

def activate():
    CUSTOM_EVALS['querylog'] = _evalPartLogger

def _evalLazyJoin(ctx, join):
    """
    A lazy join will push the variables bound
    in the first part to the second part,
    essentially doing the join implicitly
    hopefully evaluating much fewer triples
    """
    for a in evalPart(ctx, join.p1):
        c = ctx.thaw(a)
        for b in evalPart(c, join.p2):
            yield b

def _evalPartLogger(ctx, part):
    if not isinstance(ctx.graph.store, CoarseNDBStore):
        raise NotImplementedError
    if part.name == 'SelectQuery':
        s = StringIO()
        _dump(part, '', s)
        ctx.graph.store.log(s.getvalue())
        ctx.graph.store.flush_log(logging.DEBUG)
        raise NotImplementedError
    elif part.name == 'Join':
        return _evalLazyJoin(ctx, part)
    else:
        raise NotImplementedError

def _dump(part, indent, dest):
    if part is None:
        return None
    if part.name == 'BGP':
        dest.write('{}{} {} triples={}\n'.format(indent, part.name, id(part) % 10000, part.triples))
        return
    if part.name == 'Extend':
        dest.write('{}{} {} {}={}\n'.format(indent, part.name, id(part) % 10000, part.var, part.expr))
    else:
        dest.write('{}{} {}\n'.format(indent, part.name, id(part) % 10000))
    for attr in ['p', 'p1', 'p2']:
        if hasattr(part, attr):
            child  = getattr(part, attr)
            if child is not None:
                _dump(child, '{}  '.format(indent), dest)
    return

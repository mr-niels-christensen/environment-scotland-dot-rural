import logging
from rdflib.plugins.sparql.evaluate import evalPart
from rdflib.plugins.sparql import CUSTOM_EVALS
from time import time

def activate():
    CUSTOM_EVALS['querylog'] = _evalPartLogger

def deactivate():
    if 'querylog' in CUSTOM_EVALS:
        del CUSTOM_EVALS['querylog']
    
def _join(a, b, join_id):
    candidates = 0
    yielded = 0
    begin = time()
    for x in a:
        for y in b:
            candidates += 1
            if x.compatible(y):
                yielded += 1
                yield x.merge(y)
    logging.debug('Join {}: yielded {} of {} candidates, len(b)={}, in {:.1f} seconds'.format(join_id, yielded, candidates, len(b), time() - begin))

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

def _evalJoin(ctx, join):
    if join.lazy:
        logging.debug('Join {}: is lazy'.format(id(join) % 10000))
        return _evalLazyJoin(ctx, join)
    else:
        logging.debug('Join {}: made lazy'.format(id(join) % 10000))
        return _evalLazyJoin(ctx, join)
       
def _evalPartLogger(ctx, part):
    if part.name == 'SelectQuery':
        _dump(part, '')
        raise NotImplementedError
    elif part.name == 'Join':
        return _evalJoin(ctx, part)
    else:
        raise NotImplementedError

def _dump(part, indent):
    if part is None:
        return None
    if part.name == 'BGP':
        logging.debug('{}{} {} triples={}'.format(indent, part.name, id(part) % 10000, part.triples))
        return
    if part.name == 'Extend':
        logging.debug('{}{} {} {}={}'.format(indent, part.name, id(part) % 10000, part.var, part.expr))
    else:
        logging.debug('{}{} {}'.format(indent, part.name, id(part) % 10000))
    for attr in ['p', 'p1', 'p2']:
        if hasattr(part, attr):
            child  = getattr(part, attr)
            if child is not None:
                _dump(child, '{}  '.format(indent))
    return

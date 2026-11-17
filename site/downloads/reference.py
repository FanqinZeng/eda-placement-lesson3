"""Independent Manhattan net model reference. Python 3.9+, standard library only.
Run: python3 reference.py < inputs.json
inputs.json: list of nets, each net = [{"id":"A","x":2,"y":2}, ...]
Outputs [bbox, clique, star-from-first-pin] for each net.
"""
import json,sys,math,itertools
def evaluate(pins,hub=None):
    ids=[p['id'] for p in pins]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate pin')
    for p in pins:
        if any(isinstance(p[k],bool) or not isinstance(p[k],(int,float)) or not math.isfinite(p[k]) for k in ('x','y')): raise ValueError('Invalid coordinate')
    if not pins:return [0,0,0]
    hub=ids[0] if hub is None else hub
    if hub not in ids:raise ValueError('Invalid hub')
    distance=lambda a,b:abs(a['x']-b['x'])+abs(a['y']-b['y'])
    bbox=sum(max(p[k] for p in pins)-min(p[k] for p in pins) for k in ('x','y'))
    clique=sum(distance(a,b) for a,b in itertools.combinations(pins,2))
    h=next(p for p in pins if p['id']==hub)
    return [bbox,clique,sum(distance(h,p) for p in pins)]
if __name__=='__main__':print(json.dumps([evaluate(p) for p in json.load(sys.stdin)]))

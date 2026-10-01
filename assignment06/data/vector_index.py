import math
def cosine_similarity(a,b):
    if len(a)!=len(b) or not a:
        raise ValueError('Vectors must have the same nonzero dimension')
    if not all(math.isfinite(x) for x in [*a,*b]):
        raise ValueError('Vector contains a non-finite number')
    na=math.sqrt(sum(x*x for x in a));nb=math.sqrt(sum(x*x for x in b))
    return sum(x*y for x,y in zip(a,b))/(na*nb) if na and nb else 0.0
class VectorIndex:
    def __init__(self): self.vectors={}
    def add(self,product_id,vector):
        cosine_similarity(vector,vector)
        self.vectors[product_id]=list(vector)
    def retrieve(self,vector):
        return {pid:cosine_similarity(vector,v) for pid,v in self.vectors.items()}

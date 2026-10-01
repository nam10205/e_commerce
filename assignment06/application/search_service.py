from application.query_service import normalize
class SearchService:
    def __init__(self,repository,order_repository,vector_index,ranking_service):
        self.repository=repository;self.orders=order_repository
        self.index=vector_index;self.ranker=ranking_service
    def retrieve(self,query):
        similarities=self.index.retrieve(query['embedding']) if query['embedding'] is not None else {}
        candidates=[]
        for p in self.repository.all_products():
            filters=query['filters']
            if filters['max_price'] is not None and p['price']>=filters['max_price']: continue
            if filters['category'] and p['category'].lower()!=filters['category'].lower(): continue
            words=set(normalize(' '.join(str(p[k]) for k in ('name','category','color','brand','description'))).split())
            ts=sum(t in words for t in query['tokens'])/len(query['tokens']) if query['tokens'] else 0.0
            ims=max(0.0,similarities.get(p['id'],0.0))
            if (query['type'] in ('text','voice') and ts==0) or (query['type'] in ('image','multimodal') and ts==0 and ims==0): continue
            candidates.append({'product':p,'text_score':ts,'image_score':ims})
        return candidates
    def search(self,query,top_k=5):
        return self.ranker.rank(self.retrieve(query),query,top_k)
    def search_order(self,text,customer_id):
        import re
        n=normalize(text)
        if 'latest' in n.split() or 'moi nhat' in n: return self.orders.latest_order(customer_id)
        match=re.search(r'\b(?:o\d+|20\d{6})\b',n)
        return self.orders.find_order(match.group(0),customer_id) if match else None
    def view_product(self,product_id): return self.repository.find(product_id)

class RankingService:
    def rank(self,candidates,query,top_k=5):
        if not isinstance(top_k,int) or top_k<1 or top_k>100: raise ValueError('top_k must be between 1 and 100')
        ranked=[]
        for c in candidates:
            row=dict(c)
            relevance=query['weights']['text']*c['text_score']+query['weights']['image']*c['image_score']
            row['score']=0.95*relevance+0.05*(1 if c['product']['stock']>0 else 0)
            ranked.append(row)
        return sorted(ranked,key=lambda c:(-c['score'],c['product']['price'],c['product']['id']))[:top_k]

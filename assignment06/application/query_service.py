import re, unicodedata
def normalize(text):
    text=''.join(c for c in unicodedata.normalize('NFD',text.lower()) if unicodedata.category(c)!='Mn').replace('đ','d')
    return ' '.join(re.findall(r'[a-z0-9]+',text))
ALIASES={'giay':'shoes','den':'black','trang':'white','xanh':'blue','do':'red','tui':'bag','ao':'shirt','balo':'backpack','chay':'running','shoe':'shoes','bags':'bag','tshirts':'shirt','tshirt':'shirt'}
STOP={'find','me','show','products','product','for','the','a','an','please','under','below','dollars','usd','tim','cho','toi','san','pham','duoi','mau','bo'}
class QueryService:
    def _query(self,text,mode,embedding=None,max_price=None,category=None,weights=None):
        if not isinstance(text,str): raise ValueError('Text must be a string')
        normalized=normalize(text)
        match=re.search(r'\b(under|below|duoi)\s+(\d+(?:\.\d+)?)',text.lower())
        if not match: match=re.search(r'\bduoi\s+(\d+)',normalized)
        if match and max_price is None: max_price=float(match.group(2) if match.lastindex==2 else match.group(1))
        if max_price is not None and max_price<0: raise ValueError('Price cannot be negative')
        tokens=list(dict.fromkeys(ALIASES.get(t,t) for t in normalized.split() if t not in STOP and not t.isdigit()))
        if not tokens and embedding is None: raise ValueError('Query must contain meaningful keywords or an image')
        wt,wi=weights or ((0.5,0.5) if mode=='multimodal' else ((0,1) if mode=='image' else (1,0)))
        if wt<0 or wi<0 or abs(wt+wi-1)>1e-9: raise ValueError('Weights must be nonnegative and sum to 1')
        return {'type':mode,'query':text.strip(),'normalized':normalized,'tokens':tokens,'embedding':embedding,'filters':{'max_price':max_price,'category':category},'weights':{'text':wt,'image':wi}}
    def text_query(self,text,**filters): return self._query(text,'text',**filters)
    def voice_query(self,text,**filters): return self._query(text,'voice',**filters)
    def image_query(self,embedding,**filters): return self._query('','image',embedding,**filters)
    def multimodal_query(self,text,embedding,**filters): return self._query(text,'multimodal',embedding,**filters)

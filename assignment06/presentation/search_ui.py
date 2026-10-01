import json
class VoiceInput:
    def __init__(self,speech): self.speech=speech
    def read(self,transcript): return self.speech.transcribe(transcript)
class ImageUpload:
    def __init__(self,images): self.images=images
    def read(self,path): return self.images.encode(path)
class SearchResultView:
    def display(self,query,results):
        print('INPUT:',query['query'] or 'sample image')
        print('PROCESSING:',query['type'],'-> CommonQuery -> retrieval -> filtering -> ranking')
        print('TOKENS:',query['tokens'],'FILTERS:',query['filters'])
        for r in results:
            p=r['product'];print(f"{p['id']:02d} | {p['name']:<28} | ${p['price']:6.2f} | score={r['score']:.4f} | text={r['text_score']:.4f} | image={r['image_score']:.4f}")
        if not results: print('No matching products.')
class SearchUI:
    def __init__(self,queries,search,voice,upload,view):
        self.queries=queries;self.search_service=search;self.voice=voice;self.upload=upload;self.view=view
    def run(self,mode,text='',image=None,top_k=5,max_price=None,category=None,display=True):
        f={'max_price':max_price,'category':category}
        if mode=='text': q=self.queries.text_query(text,**f)
        elif mode=='voice': q=self.queries.voice_query(self.voice.read(text),**f)
        elif mode=='image': q=self.queries.image_query(self.upload.read(image),**f)
        elif mode=='multimodal': q=self.queries.multimodal_query(text,self.upload.read(image),**f)
        else: raise ValueError('Unsupported mode')
        results=self.search_service.search(q,top_k)
        if display: self.view.display(q,results)
        return q,results
    def search_order(self,text,customer_id): return self.search_service.search_order(text,customer_id)
    def view_product(self,product_id): return self.search_service.view_product(product_id)

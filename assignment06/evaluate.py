"""A fixed, transparent 12-query functional evaluation; not an accuracy benchmark."""
import csv,json
from main import create_ui,BASE
def evaluate():
    ui=create_ui()
    # Expected sets are declared before results are computed.
    cases=[
        ('T01','text','black shoes',None,{1,5}),
        ('T02','voice','find running shoes',None,{1,2,4}),
        ('T03','image','', 'query_black_shoe.png',{1,5}),
        ('T04','text','find Nike shoes under 100 dollars',None,{5}),
        ('T05','text','white shirt',None,{7}),
        ('T06','text','blue backpack',None,{9}),
        ('T07','multimodal','black shoes','query_black_shoe.png',{1,5}),
        ('T08','order','find order O001',None,{'O001'}),
        ('T09','order','where is my latest order',None,{'20261001'}),
        ('T10','text','spaceship',None,{None}),
        # Two challenge queries expose spelling and phrase-understanding limits.
        ('T11','text','sneekers',None,{1,2,4,5,6}),
        ('T12','text','not black shoes',None,{2,4,6})]
    rows=[]
    for cid,mode,text,img,expected in cases:
        if mode=='order':
            o=ui.search_order(text,'C001');top=o['order_id'] if o else None;name=top;score=None
        else:
            _,r=ui.run(mode,text,BASE/'data/dataset/images'/img if img else None,display=False)
            top=r[0]['product']['id'] if r else None;name=r[0]['product']['name'] if r else 'No results';score=r[0]['score'] if r else None
        rows.append({'id':cid,'mode':mode,'input':text or img,'expected_top1':sorted(expected,key=str),'actual_top1':top,'name':name,'score':score,'success':top in expected})
    passed=sum(r['success'] for r in rows)
    summary={'metric':'Top-1 success on fixed hand-labeled fixture queries (correct empty output counts)','total':len(rows),'successful':passed,'success_rate':passed/len(rows),'cases':rows}
    (BASE/'demo/evaluation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    with (BASE/'demo/evaluation.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary
if __name__=='__main__':evaluate()

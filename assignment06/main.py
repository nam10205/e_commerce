import argparse, json
from pathlib import Path
from data.product_repository import ProductRepository
from data.order_repository import OrderRepository
from data.vector_index import VectorIndex
from application.query_service import QueryService
from application.speech_service import SpeechService
from application.image_service import ImageService
from application.ranking_service import RankingService
from application.search_service import SearchService
from presentation.search_ui import SearchUI,VoiceInput,ImageUpload,SearchResultView
BASE=Path(__file__).parent
def create_ui():
    repository=ProductRepository();image_service=ImageService();index=VectorIndex()
    for p in repository.all_products(): index.add(p['id'],image_service.encode(repository.image_path(p)))
    search=SearchService(repository,OrderRepository(),index,RankingService())
    return SearchUI(QueryService(),search,VoiceInput(SpeechService()),ImageUpload(image_service),SearchResultView())
def demo(ui):
    print('=== ASSIGNMENT 06: MULTIMODAL E-COMMERCE SEARCH ===')
    entries=[]
    for mode,text,img in [('text','black shoes',None),('voice','find running shoes',None),('image','',BASE/'data/dataset/images/query_black_shoe.png'),('multimodal','black shoes',BASE/'data/dataset/images/query_black_shoe.png')]:
        print('\nMODE:',mode.upper())
        q,r=ui.run(mode,text,img,top_k=3);entries.append({'query':q,'results':r})
    print('\nORDER:',json.dumps(ui.search_order('find my order 20261001','C001'),ensure_ascii=False))
    path=BASE/'demo/demo_results.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Three-layer multimodal search prototype')
    parser.add_argument('--mode',choices=['text','voice','image','multimodal','order','product'])
    parser.add_argument('--query',default='');parser.add_argument('--image')
    parser.add_argument('--max-price',type=float);parser.add_argument('--category')
    parser.add_argument('--top-k',type=int,default=5);parser.add_argument('--customer',default='C001')
    parser.add_argument('--product-id',type=int)
    args=parser.parse_args();ui=create_ui()
    try:
        if not args.mode: demo(ui)
        elif args.mode=='order': print(json.dumps(ui.search_order(args.query,args.customer),ensure_ascii=False,indent=2))
        elif args.mode=='product':
            if args.product_id is None: parser.error('product mode requires --product-id')
            print(json.dumps(ui.view_product(args.product_id),ensure_ascii=False,indent=2))
        else: ui.run(args.mode,args.query,args.image,args.top_k,args.max_price,args.category)
    except ValueError as exc: parser.error(str(exc))

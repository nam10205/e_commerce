"""Local HTML presentation; uses only the injected SearchUI facade."""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit,parse_qs
import html
class WebHandler(BaseHTTPRequestHandler):
    ui=None
    image_path=None
    def do_GET(self):
        params=parse_qs(urlsplit(self.path).query,keep_blank_values=True)
        mode=params.get('mode',['text'])[0];text=params.get('query',['black shoes'])[0]
        rows='';processing='';error=''
        try:
            if mode=='order':
                o=self.ui.search_order(text,'C001')
                rows='<tr><td colspan="5">'+html.escape(str(o) if o else 'No order found for customer C001')+'</td></tr>'
                processing='Search Order → customer-scoped repository → order status'
            else:
                q,r=self.ui.run(mode,text,self.image_path,top_k=5,display=False)
                processing=html.escape(f"{q['type']} → CommonQuery → retrieval → filtering → ranking | tokens: {q['tokens']}")
                for row in r:
                    p=row['product'];rows+=f"<tr><td>{p['id']}</td><td>{html.escape(p['name'])}</td><td>${p['price']:.2f}</td><td>{row['score']:.4f}</td><td>text {row['text_score']:.4f} / image {row['image_score']:.4f}</td></tr>"
                if not r:rows='<tr><td colspan="5">No matching products</td></tr>'
        except ValueError as exc:error=html.escape(str(exc))
        opts=''.join(f'<option {"selected" if x==mode else ""}>{x}</option>' for x in ['text','voice','image','multimodal','order'])
        page=f'''<!DOCTYPE html><html lang="vi"><meta charset="utf-8"><title>Assignment 06 Search Demo</title>
        <style>body{{background:#eef3f8;color:#183049;font:18px Arial;margin:0}}main{{max-width:1120px;margin:45px auto}}h1{{font-size:36px}}small{{color:#53677c}}form,.panel{{background:white;padding:25px;border-radius:12px;margin:24px 0}}input,select,button{{font-size:19px;padding:12px;margin:8px 12px 8px 0;border:1px solid #a8b8c8;border-radius:5px}}input{{width:52%}}button{{background:#155f9b;color:white}}table{{width:100%;border-collapse:collapse}}td,th{{text-align:left;padding:17px 10px;border-bottom:1px solid #dce4ec}}th{{background:#edf4fa}}.process{{line-height:1.6;color:#3e5f7a}}.tag{{background:#d8ecfd;padding:8px;border-radius:5px}}</style>
        <main><small>INFORMATION SYSTEM ANALYSIS AND DESIGN · ASSIGNMENT 06</small><h1>Multimodal E-Commerce Search</h1><p>Text · Simulated voice · Image similarity · Multimodal fusion</p>
        <form><label>Mode <select name="mode">{opts}</select></label><input name="query" value="{html.escape(text,quote=True)}"><button>Search</button><p><small>Voice uses a typed transcript. Image modes use query_black_shoe.png, a generated shoe fixture. Order queries run as C001.</small></p></form>
        <div class="panel"><span class="tag">Live Python results</span><p class="process">{processing}</p><p>{error}</p><table><tr><th>ID</th><th>Product / Order</th><th>Price</th><th>Ranking score</th><th>Signals</th></tr>{rows}</table></div>
        <p><small>Presentation → Application / Intelligence → Data · deterministic ranking · 12 products</small></p></main></html>'''
        self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(page.encode('utf-8'))

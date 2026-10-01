from http.server import HTTPServer
from main import create_ui,BASE
from presentation.web_ui import WebHandler
if __name__=='__main__':
    WebHandler.ui=create_ui()
    WebHandler.image_path=BASE/'data/dataset/images/query_black_shoe.png'
    print('Open http://127.0.0.1:8765 . Press Ctrl+C to stop.',flush=True)
    HTTPServer(('127.0.0.1',8765),WebHandler).serve_forever()

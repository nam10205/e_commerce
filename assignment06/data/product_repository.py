import json
from pathlib import Path
class ProductRepository:
    def __init__(self, path=None):
        self.base = Path(path).parent if path else Path(__file__).parent / 'dataset'
        self.products = json.loads((Path(path) if path else self.base/'products.json').read_text(encoding='utf-8'))
        ids = [p['id'] for p in self.products]
        if len(ids) != len(set(ids)):
            raise ValueError('Duplicate product IDs')
    def all_products(self):
        return [dict(p) for p in self.products]
    def find(self, product_id):
        return next((dict(p) for p in self.products if p['id']==product_id),None)
    def image_path(self, product):
        return self.base / product['image']

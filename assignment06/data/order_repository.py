import json
from pathlib import Path
class OrderRepository:
    def __init__(self):
        self.orders=json.loads((Path(__file__).parent/'dataset/orders.json').read_text(encoding='utf-8'))
    def find_order(self, order_id, customer_id):
        return next((dict(o) for o in self.orders if o['order_id'].upper()==order_id.upper() and o['customer_id']==customer_id),None)
    def latest_order(self, customer_id):
        rows=[o for o in self.orders if o['customer_id']==customer_id]
        return dict(max(rows,key=lambda o:(o['date'],o['order_id']))) if rows else None

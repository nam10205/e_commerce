import unittest
from pathlib import Path
from main import create_ui, BASE
from data.vector_index import cosine_similarity
from application.query_service import QueryService
class SystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.ui=create_ui()
    def test_text_and_simulated_voice_equivalent(self):
        _,a=self.ui.run('text','black shoes',display=False)
        _,b=self.ui.run('voice','black shoes',display=False)
        self.assertEqual(a,b)
    def test_price_filter_is_strict(self):
        _,r=self.ui.run('text','find Nike shoes under 100 dollars',display=False)
        self.assertEqual(r[0]['product']['id'],5)
        self.assertTrue(all(x['product']['price']<100 for x in r))
    def test_image_retrieval(self):
        _,r=self.ui.run('image',image=BASE/'data/dataset/images/query_black_shoe.png',display=False)
        self.assertEqual(r[0]['product']['id'],5)
        self.assertGreater(r[0]['image_score'],0.99)
    def test_order_is_scoped_to_customer(self):
        self.assertIsNone(self.ui.search_order('order O002','C001'))
        self.assertEqual(self.ui.search_order('order O002','C002')['status'],'Delivered')
    def test_latest_order(self):
        self.assertEqual(self.ui.search_order('where is my latest order','C001')['order_id'],'20261001')
    def test_empty_query_rejected(self):
        with self.assertRaises(ValueError):self.ui.run('text','   ',display=False)
    def test_unknown_keywords_empty(self):
        _,r=self.ui.run('text','spaceship',display=False);self.assertEqual(r,[])
    def test_category_filter(self):
        _,r=self.ui.run('text','black',category='shoes',display=False)
        self.assertTrue(r);self.assertTrue(all(x['product']['category']=='shoes' for x in r))
    def test_cosine_zero_and_dimensions(self):
        self.assertEqual(cosine_similarity([0,0],[1,2]),0)
        with self.assertRaises(ValueError):cosine_similarity([1],[1,2])
    def test_multimodal_weight_validation(self):
        with self.assertRaises(ValueError):QueryService().multimodal_query('black',[1],weights=(0.8,0.8))
    def test_stock_signal(self):
        _,r=self.ui.run('text','running shoes',top_k=12,display=False)
        by_id={x['product']['id']:x for x in r}
        self.assertEqual(by_id[6]['score'],0.95)
        self.assertEqual(by_id[1]['score'],1.0)
    def test_bad_image_rejected(self):
        with self.assertRaises(ValueError):self.ui.run('image',image='missing.png',display=False)
    def test_topk_validation(self):
        with self.assertRaises(ValueError):self.ui.run('text','shoes',top_k=0,display=False)
if __name__=='__main__': unittest.main()

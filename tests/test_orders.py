import unittest
import json
from app import create_app


class TestOrders(unittest.TestCase):
    def setUp(self):
        '''set the app for testing
        setting a test client for testing'''

        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):

        self.app_context.pop()

    def test_create_food(self):
        data = {"name": "eggcurry", "price": 20, "description": "sweet eggs"}

        res = self.client.post(
            "/api/v1/fooditem",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)['message'], "Food item created")

    def test_post_order(self):
        data = {
            "username": "kelvin",
            "destination": "juja",
            "name": "ugali",
            "description": "smashed",
            "price": 20
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 201)

    def test_get_all_orders(self):
        '''get all placed orders'''
        self.post_order()
        res = self.client.get(
            "/api/v1/orders", headers={"content-type": "application/json"})
        print(res.data)
        self.assertEqual(res.status_code, 200)

    def get_all_food_items(self):
        '''get food items created'''
        res = self.client.get(
            "/api/v1/fooditems", headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 200)

    def post_order(self):
        data = {
            "username": "kelvin",
            "destination": "juja",
            "name": "ugali",
            "description": "smashed",
            "price": 20
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json"})
        return res

    def test_order_by_id(self):
        '''get order by id'''

        res = self.client.get(
            "/api/v1/orders/1", headers={"content-type": "application/json"})

        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_mark_order_as_completed(self):
        '''test for orders completed by admin'''

        res = self.client.put(
            "/api/v1/orders/1/complete",
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            json.loads(res.data)['message'], "please approve the order first ")

    def test_declined_orders_by_admin(self):
        '''test for returning a list for orders declined by admin'''

        res = self.client.get(
            "/api/v1/orders/declined",
            headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 200)

    def test_get_accepted_orders(self):
        '''test for getting a list of all orders accepted by admin'''

        res = self.client.get(
            "/api/v1/orders/approved",
            headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 200)

    def test_update_status_approved(self):
        '''test for an order whose status has been approved'''

        self.post_order()
        res = self.client.put(
            "/api/v1/orders/1/approve",
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            json.loads(res.data)['message'], "your order has been approved")

    def test_completed_orders(self):
        '''test for returning a list of completed orders'''

        res = self.client.get(
            "/api/v1/orders/completed",
            headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 200)

    def test_non_order_by_id(self):
        '''testing for a an order that doesn't exist'''

        res = self.client.get(
            "/api/v1/orders/111", headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)['message'], "Order not found")

    def test_non_order_delete(self):
        '''deleting an order that doesn't exist'''

        res = self.client.delete(
            "api/v1/orders/1111111111",
            headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)['message'], "Order not found")

    def test_declined_orders_list(self):
        '''testing for declined order'''

        res = self.client.get(
            "/api/v1/orders/declined",
            headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 200)

    def test_invalid_name(self):
        '''test for invalid food name'''
        data = {"name": "******", "price": 20, "description": "sweet eggs"}

        res = self.client.post(
            "/api/v1/fooditem",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            json.loads(res.data)['message'], "Food name is invalid")

    def test_invalid_description(self):
        '''test for invalid food description'''
        data = {"name": "ugali", "price": 20, "description": "^^^^^&#####"}

        res = self.client.post(
            "/api/v1/fooditem",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            json.loads(res.data)['message'], "invalid food description")

    def test_invalid_price(self):
        '''test for invalid food description'''
        data = {"name": "ugali", "price": "****", "description": "sweet"}

        res = self.client.post(
            "/api/v1/fooditem",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)['message'], "Invalid price")

    def test_invalid_username(self):
        data = {
            "username": "******",
            "destination": "juja",
            "name": "ugali",
            "description": "smashed",
            "price": 20
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            json.loads(res.data)['message'], "Please enter  a valid name")

    def test_invalid_destination(self):
        data = {
            "username": "kelvin",
            "destination": "#$$$#$#@###",
            "name": "ugali",
            "description": "smashed",
            "price": 20
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            json.loads(res.data)['message'],
            "please enter a valid destination")

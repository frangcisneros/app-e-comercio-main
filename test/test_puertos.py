import unittest
from app import create_app, db
import requests


class PuertosTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_puerto(self):
        response = requests.get("http://localhost:5000/api/v1/stock")
        self.assertEqual(response.status_code, 200)

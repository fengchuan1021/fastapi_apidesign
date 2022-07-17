import unittest
from fastapi.testclient import TestClient
from app import app
from modules.frontend.user import UserController
import settings
class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        print(f'{settings.DEBUG=}')
    def test_register(self):

        ret=self.client.post(UserController.router.prefix+'/register',json={"username":"fengchuan3","password":"1234564","repassword":"123456","phone":"16603818316"})
        print(ret.json())
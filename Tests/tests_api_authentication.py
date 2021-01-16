import unittest

import Routes
from Tests.data_api_tests import DataApi
from Tests.data_utils import set_test_database_data, clear_test_database


class TestApiAuthentication(unittest.TestCase):
  def setUp(self):
    Routes.app.testing = True
    self.app = Routes.app.test_client()

  def tearDown(self):
    super().tearDown()

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    set_test_database_data('users', DataApi.API_TOKEN)

  @classmethod
  def tearDownClass(cls):
    super().tearDownClass()
    clear_test_database('users')

  def test_wrong_api_token(self):
    res = self.app.get('api/v1/isalive', headers={'SECURITY_TOKEN_AUTHENTICATION_KEY': '123abc'})
    self.assertEqual(401, res.status_code)
    
  def test_wrong_api_token_empty(self):
    res = self.app.get('api/v1/isalive', headers={})
    self.assertEqual(401, res.status_code)

  def test_access(self):
    res = self.app.get('api/v1/isalive', headers={'SECURITY_TOKEN_AUTHENTICATION_KEY': 'ExampleAccess'})
    self.assertEqual(200, res.status_code)

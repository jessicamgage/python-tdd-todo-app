from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token
import accounts.views

@patch('accounts.views.auth')
class LoginViewTest(TestCase):
	def test_redirects_to_home_page(self, mock_auth):
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertRedirects(response, '/')

	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(
			mock_auth.authenticate.call_args,
			call(uid='abcd123')
		)
	
	def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(
			mock_auth.login.call_args,
			call(response.wsgi_request, mock_auth.authenticate.return_value)
		)

	def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
		mock_auth.authenticate.return_value = None
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(mock_auth.login.called, False)

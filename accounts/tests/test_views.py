from django.test import TestCase
from unittest.mock import patch
from accounts.models import Token
import accounts.views

class SendLoginEmailViewTest(TestCase):
	def test_redirects_to_home_page(self):
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertRedirects(response, '/')

	def test_adds_success_message(self):
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'onlyforbook61@gmail.com'
		}, follow=True)

		message = list(response.context['messages'])[0]
		self.assertEqual(
			message.message,
			"Check your email, we've sent you a link you can use to log in."
		)
		self.assertEqual(message.tags, "success")


	def test_creates_token_associated_with_email(self):
		self.client.post('/accounts/send_login_email', data={
			'email': 'onlyforbook61@gmail.com'
		})
		token = Token.objects.first()
		self.assertEqual(token.email, 'onlyforbook61@gmail.com')

	@patch('accounts.views.send_mail')
	def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
		self.client.post('/accounts/send_login_email', data={
			'email': 'onlyforbook61@gmail.com'
		})

		token = Token.objects.first()
		expected_url = f'http://testserver/accounts/login?token={token.uid}'

		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertIn(expected_url, body)

	@patch('accounts.views.send_mail')
	def test_sends_mail_to_address_from_post(self, mock_send_mail):
		self.client.post('/accounts/send_login_email', data={
			'email': 'onlyforbook61@gmail.com'
		})

		self.assertEqual(mock_send_mail.called, True)
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertEqual(subject, 'Your login link for TheToDoListSite')
		self.assertEqual(from_email, 'noreply@thetodolistsite')
		self.assertEqual(to_list, ['onlyforbook61@gmail.com'])

from django.test import TestCase
import accounts.views

class SendLoginEmailViewTest(TestCase):
	def test_redirects_to_home_page(self):
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'onlyforbook61@gmail.com'
		})
		self.assertRedirects(response, '/')

	def test_sends_mail_to_address_from_post(self):
		self.send_mail_called = False

		def fake_send_login_email(subject, body, from_email, to_list):
			self.send_mail_called = True
			self.subject = subject
			self.body = body
			self.from_email = from_email
			self.to_list = to_list

		accounts.views.send_mail = fake_send_login_email

		self.client.post('/accounts/send_login_email', data={
			'email': 'onlyforbook61@gmail.com'
		})

		self.assertTrue(self.send_mail_called)
		self.assertEqual(self.subject, 'Your login link for TheToDoListSite')
		self.assertEqual(self.from_email, 'noreply@thetodolistsite')
		self.assertEqual(self.to_list, ['onlyforbook61@gmail.com'])

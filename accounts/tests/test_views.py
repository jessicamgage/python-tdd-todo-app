from django.test import TestCase

class SendLoginEmailViewTest(TestCase):
	def test_redirects_to_home_page(self):
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'onlyforbook61@gmail.com'
		})
		self.assertRedirects(response, '/')

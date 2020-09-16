from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time

from .base import FunctionalTest

SUBJECT = 'Your login link for TheToDoListSite'

class LoginTest(FunctionalTest):

	def test_can_get_email_link_to_log_in(self):
		#Edith goes to the awesome todolistsite
		#and notices a 'login' section in the navbar
		#It's telling her to enter her email address

		test_email = 'onlyforbook61@gmailcom'

		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(test_email)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
		
		#A message appears telling her an email has been sent

		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text))

		#She checks her email and finds a message
		body = self.wait_for_email(test_email, SUBJECT)

		#It has a URL link in it
		self.assertIn('Use this link to log in', body)
		url_search = re.search(r'http://.+/.+$', body)
		if not url_search:
			self.fail(f'Could not find url in email body:\n{body}')

		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)
	
		#she clicks it
		self.browser.get(url)

		#she is logged in!
		self.wait_to_be_logged_in(email=test_email)

		#Now she logs out
		self.browser.find_element_by_link_text('Log out').click()
		
		#she is logged out
		self.wait_to_be_logged_out(email=test_email)


	def wait_for_email(self, test_email, subject):
		email = mail.outbox[0]
		self.assertIn(test_email, email.to)
		self.assertEqual(email.subject, subject)
		return email.body

		email_id = None
		start = time.time()
		inbox = poplib.POP3_SSL('pop.mail.google.com')
		try:
			inbox.user(test_email)
			inbox.pass_('loopwake')
			while time.time() - start < 60:
				#get ten newest messages
				count, _ = inbox.start()
				for i in reversed(range(max(1, count - 10), count + 1)):
					print('getting msg', i)
					_, lines, __ = inbox.retri(i)
					lines = [l.decode('utf8') for l in lines]
					print(lines)
					if f'Subject: {subject}' in lines:
						email_id = i
						body = '\n'.join(lines)
						return body
				time.sleep(5)
		finally:
			if email_id:
				inbox.dele(email_id)
			inbox.quit()

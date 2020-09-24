from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from unittest import skip
from selenium.common.exceptions import WebDriverException
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

import os

MAX_WAIT = 10
User = get_user_model()

class FunctionalTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def add_list_item(self, item_text):
		num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
		self.get_item_input_box().send_keys(item_text)
		self.get_item_input_box().send_keys(Keys.ENTER)
		item_number = num_rows + 1
		self.wait_for_row_in_list_table(f'{item_number}: {item_text}')


	def wait(fn):
		def modified_fn(*args, **kwargs):
			start_time = time.time()
			while True:
				try:
					return fn(*args, **kwargs)
				except (AssertionError, WebDriverException) as e:
					if time.time() - start_time > MAX_WAIT:
						raise e
					time.sleep(0.5)
	
		return modified_fn
	
	def create_pre_authenticated_session(self, email):
                user = User.objects.create(email=email)
                session = SessionStore()
                session[SESSION_KEY] = user.pk
                session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
                session.save()

                self.browser.get(self.live_server_url + "/404_no_such_url/")
                self.browser.add_cookie(dict(
                        name=settings.SESSION_COOKIE_NAME,
                        value=session.session_key,
                        path='/',
                ))

	
	@wait
	def wait_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	@wait
	def wait_for(self, fn):
		return fn()

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)


	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element_by_name('email')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)

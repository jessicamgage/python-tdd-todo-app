from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from unittest import skip

from selenium.common.exceptions import WebDriverException

import os

class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server	

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		time.sleep(2)

		table = self.browser.find_element_by_id('id_list_table')
			
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
		return


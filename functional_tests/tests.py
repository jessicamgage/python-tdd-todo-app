from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.common.exceptions import WebDriverException

import os

class NewVisitorTest(StaticLiveServerTestCase):

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

	def test_layout_and_styling(self):
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=1000
		)

		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_elements_by_css_selector('id_new_item')

	def test_can_start_a_list_for_one_user(self):
		#Edith has heard about a cool new to-do app. She goes to check out its homepage
		
		self.browser.get(self.live_server_url)

		#She notices the page title and header mention to-do lists

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text

		self.assertIn('To-Do', header_text)

		#She is invited to enter a to-do item immediately

		inputbox = self.browser.find_element_by_id('id_new_item')

		#She types 'Buy peacock feathers' into a textbox

		inputbox.send_keys('Buy peacock feathers')

		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')


		#When she hits enter, the page updates, and now the page lists 1: Buy peacock feathers as an item in the to-do list

		#There is still a text box inviting her to add another item. She enters 'Use peacock feathers to make a fly'

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		#The page updates again and shows both items

		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		#She wonders iwhether the site will remember her list. Then she notices that the site has generated a unique URL for her.

		# She visits that URL and her to-do list is still there

		#She goes back to sleep

	def test_multiple_users_can_start_lists_at_different_urls(self):
		#Edith starts a new to-do-list
		self.browser.get(self.live_server_url)
		
		inputbox = self.browser.find_element_by_id('id_new_item')

		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		#She notices that her list has a unique URL

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#Now, a new user, Francis, comes to the site.

		##We use a new browser session to make sure that no information
##of Edith's is coming from cookies, etc

		self.browser.quit()
		self.browser = webdriver.Firefox()

		#Francis visits the home page. There is no sign of Edith's list

		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		#Francis starts a new list by entering a new item. He is less 
#interesting than Edith...

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy almond milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy almond milk')

		#Francis gets his own unique URL

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#Again, there is no trace of Edith's list

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy almond milk', page_text)

		#They both go back to sleep

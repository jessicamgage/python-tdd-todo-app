from .base import FunctionalTest

class MyListsTest(FunctionalTest):
	def test_logged_in_user_lists_are_saved_as_my_lists(self):

		#Edith is a logged-in user
		self.create_pre_authenticated_session('edith@example.com')
	
		#She goes to the home page and starts a list
		self.browser.get(self.live_server_url)
		self.add_list_item('Reticulate splines')
		self.add_list_item('Immanentize eschaton')
		first_list_url = self.browser.current_url

		#She notices a 'My lists' link
		self.browser.find_element_by_link_text('My lists').click()

		#She sees that her list is there, named according to its first list item

		self.wait_for(lambda:
			self.browser.find_element_by_link_text('Reticulate splines')
		)
		
		self.browser.find_element_by_link_text('Reticulate splines').click()

		self.wait_for(lambda:
			self.assertEqual(self.browser.current_url, first_list_url)
		)


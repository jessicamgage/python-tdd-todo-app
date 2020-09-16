from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest

User = get_user_model()

class MyListsTest(FunctionalTest):
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

		#She decides to start another list, just to see
		self.browser.get(self.live_server_url)
		self.add_list_item('Click cows')
		second_list_url = self.browser.current_url

		#Under 'My Lists', her new list appears
		self.browser.find_element_by_link_text('Click cows').click()
		self.wait_for(lambda:
			self.browser.find_element_by_link_text('Click cows')
		)
		self.browser.find_element_by_link_text('Click cows').click()
		self.wait_for(lambda:
			self.assertEqual(self.browser.current_url, second_list_url)
		)

		#She logs out. The 'my lists' option disappears
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_link_text('My lists'), []
		))

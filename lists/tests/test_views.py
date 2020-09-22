from django.template.loader import render_to_string
from django.urls import resolve
from django.http import HttpRequest
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import (EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm, ItemForm)
from django.contrib.auth import get_user_model
from unittest.mock import patch, Mock
from unittest import TestCase
from django.test import TestCase as DjangoTestCase

from lists.views import home_page
from lists.views import new_list

User = get_user_model()

@patch('lists.views.NewListForm')
class NewListViewUnitTest(TestCase):
	def setUp(self):
		self.request = HttpRequest()
		self.request.POST['text'] = 'new list item'
		self.request.user = Mock()

	def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
		new_list(self.request)
		mockNewListForm.assert_called_once_with(data=self.request.POST)

	def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = True
		new_list(self.request)
		mock_form.save_assert_called_once_with(owner=self.request.user)

	@patch('lists.views.redirect')
	def test_redirects_to_form_returned_object_if_form_valid(
		self, mock_redirect, mockNewListForm
	):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.returned_value = True
		
		response = new_list(self.request)
	
		self.assertEqual(response, mock_redirect.return_value)
		mock_redirect.assert_called_once_with(mock_form.save.return_value)

	@patch('lists.views.render')
	def test_renders_to_home_page_if_form_invalid(
		self, mock_render, mockNewListForm
	):

		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = False

		response = new_list(self.request)
	
		self.assertEqual(response, mock_render.return_value)
		mock_render.assert_called_once_with(
			self.request, 'home.html', {'form': mock_form}
		)

	def test_does_not_save_if_form_invalid(self, mockNewListForm):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = False
		new_list(self.request)
		self.assertFalse(mock_form.save.called)

	@patch('lists.views.redirect')
	def test_redirects_to_form_returned_objects_if_form_valid(
		self, mock_redirect, mockNewListForm
	):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = True
		
		response = new_list(self.request)

		
		self.assertEqual(response, mock_redirect.return_value)
		mock_redirect.assert_called_once_with(mock_form.save.return_value)

class NewListViewIntegratedTest(DjangoTestCase):
	def test_can_save_a_POST_request(self):
                response = self.client.post('/lists/new', data={'text': 'A new list item'})
                self.assertEqual(Item.objects.count(), 1)
                new_item = Item.objects.first()
                self.assertEqual(new_item.text, 'A new list item')

	
	def test_for_invalid_input_doesnt_save_but_shows_errors(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

class NewListTest(DjangoTestCase):
	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_displays_item_form(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertIsInstance(response.context['form'], ExistingListItemForm)
		self.assertContains(response, 'name="text"')

	def test_list_owner_is_saved_if_user_is_authenticated(self):

		user = User.objects.create(email='a@b.com')
		self.client.force_login(user)
		self.client.post('/lists/new', data={'text': 'new item'})
		list_ = List.objects.first()
		self.assertEqual(list_.owner, user)


class MyListsTest(DjangoTestCase):
	def test_my_lists_url_renders_to_my_lists_template(self):
		User.objects.create(email='a@b.com')
		response = self.client.get('/lists/users/a@b.com/')
		self.assertTemplateUsed(response, 'my_lists.html')

	def test_passes_correct_owner_to_template(self):
		User.objects.create(email='wrong@owner.com')
		correct_user = User.objects.create(email='right@owner.com')
		response = self.client.get('/lists/users/right@owner.com/')
		self.assertEqual(response.context['owner'], correct_user)

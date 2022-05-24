from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page #(2)
from lists.models import Item
class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item=Item()
		first_item.text='The first (ever) list item'
		first_item.save()

		second_item=Item()
		second_item.text='Item the second'
		second_item.save()

		save_items = Item.objects.all()
		self.assertEqual(save_items.count(),2)

		first_save_item = save_items[0]
		second_save_item = save_items[1]
		self.assertEqual(first_save_item.text,'The first (ever) list item')
		self.assertEqual(second_save_item.text,'Item the second')
class HomePageTest(TestCase):
	def test_root_url_resolve_to_home_page_view(self):
		found  =resolve('/') #(1)
		self.assertEqual(found.func,home_page)#(1)
	def test_home_page_returns_correct_html(self):
		response= self.client.get('/')
		self.assertTemplateUsed(response,'home.html')
	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response,'home.html')

	def test_redirects_after_POST(self):
		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertEqual(response.status_code,302)
		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

	def test_only_saves_items_when_necessary(self):
		self.client.get('/')
		self.assertEqual(Item.objects.count(),0)

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response,'list.html')
	def test_displays_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response,'itemey 1')
		self.assertContains(response,'itemey 2')




from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)

		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def home_page(request):
		if request.method == 'POST':
			new_item_text = request.POST['item_text']
			Item.objects.create(text=new_item_text)
		else:
			new_item_text = ''
		return render(request, 'home.html', {
			'new_item_text': new_item_text,
		})

class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
			)
		self.assertRedirects(response, '/lists/the_only_list_in_the_world/')



class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the_only_list_in_the_world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		Item.objects.create(text='itemy 1')
		Item.objects.create(text='itemy 2')

		response = self.client.get('/lists/the_only_list_in_the_world/')

		self.assertContains(response, 'itemy 1')
		self.assertContains(response, 'itemy 2')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
    	list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_lists = List.objects.all()
        self.assertEqual(saved_lists.count(), 1)
        self.assertEqual(saved_lists[0], list_)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)




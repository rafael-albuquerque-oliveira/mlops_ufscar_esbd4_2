from django.urls import resolve  # Consider using reverse() if URL names are defined.
from django.test import TestCase
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
    """
    Tests for the home page view.
    """

    def test_root_url_resolves_to_home_page_view(self):
        """
        Test that the root URL ('/') resolves to the home_page view.
        """
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        Test that a GET request to the home page returns the correct HTML using the 'home.html' template.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        """
        Test that a GET request to the home page does not save any items to the database.
        """
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):
    """
    Tests for creating a new list.
    """

    def test_can_save_a_post_request(self):
        """
        Test that a POST request to '/lists/new' saves a new item in the database.
        """
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """
        Test that after a POST request to create a new list, the user is redirected to the new list's page.
        """
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTests(TestCase):
    """
    Tests for adding a new item to an existing list.
    """

    def test_can_save_a_post_request_to_an_existing_list(self):
        """
        Test that a POST request to add an item to an existing list saves the new item correctly.
        """
        # Create two lists; the new item should be added only to the correct one.
        List.objects.create()  # Extra list to ensure separation.
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """
        Test that after adding an item, the user is redirected to the list view.
        """
        List.objects.create()  # Extra list to ensure separation.
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')


class ListViewTest(TestCase):
    """
    Tests for the list view which displays items of a specific list.
    """

    def test_uses_list_template(self):
        """
        Test that the list view uses the 'list.html' template.
        """
        list_obj = List.objects.create()
        response = self.client.get(f'/lists/{list_obj.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        """
        Test that the list view displays only the items associated with the correct list.
        """
        # Create a list and add two items to it.
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)

        # Create another list with different items.
        other_list = List.objects.create()
        Item.objects.create(text='Other list item 1', list=other_list)
        Item.objects.create(text='Other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Other list item 1')
        self.assertNotContains(response, 'Other list item 2')

    def test_passes_correct_list_to_template(self):
        """
        Test that the view passes the correct list to the template context.
        """
        List.objects.create()  # Extra list to ensure separation.
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

class ListAndItemModelTest(TestCase):
    """
    Tests for the List and Item models.
    """

    def test_saving_and_retrieving_items(self):
        """
        Test that items can be saved and retrieved correctly from the database and that they are associated with the correct list.
        """
        # Create a new list.
        list_obj = List.objects.create()

        # Create two items associated with this list.
        Item.objects.create(text='The first (ever) list item', list=list_obj)
        Item.objects.create(text='The second item', list=list_obj)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_obj)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_obj)
        self.assertEqual(second_saved_item.text, 'The second item')
        self.assertEqual(second_saved_item.list, list_obj)

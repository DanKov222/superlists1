from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from .models import Item

from .views import home_page


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_home_page_returns_correct_html(self):
        """Тест: домашняя страница возвращает правильный html"""
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertIn('<title>To-Do lists</title>', html)

        self.assertTemplateUsed(response, 'lists/home_page.html')    # проверка шаблона

    def test_uses_home_template(self):
        """Тест: используется домашний шаблон"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home_page.html')

    def test_can_save_a_POST_request(self):
        """Тест: можно сохранить POST-запрос"""
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST_request(self):
        """Тест: проверка переадресации после POST запроса"""
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/single_list/')

    def test_only_saves_items_when_necessary(self):
        """Тест: сохраняет элементы, только когда нужно"""
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    """Тест модели элемента списка"""

    def test_saving_and_retrieving_items(self):
        """Тест: сохранения и получения элементов списка"""
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second Item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'The second Item')


class ListViewTest(TestCase):
    """Тест: представление списка"""

    def test_displays_all_items(self):
        """Тест: отображает все элементы списка"""
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/single_list/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

    def test_uses_list_template(self):
        """Тест: используется шаблон списка"""
        response = self.client.get('/lists/single_list/')
        self.assertTemplateUsed(response, 'lists/list.html')

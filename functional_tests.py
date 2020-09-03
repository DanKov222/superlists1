from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    """Тест нового пользователя"""

    def setUp(self):
        """Установка браузера"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Деинсталирование"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест: можно ли начать список и получить его позже"""
        self.browser.get('http://127.0.0.1:8000/')

        self.assertIn('To-Do lists', self.browser.title)
        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
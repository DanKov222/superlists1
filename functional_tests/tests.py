from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase


MAX_WAIT = 10   # Максимальное время ожидания


class NewVisitorTest(LiveServerTestCase):
    """Тест нового пользователя"""

    def setUp(self):
        """Установка браузера"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Деинсталирование"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Ожидание элемента в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест: можно ли начать список и получить его позже"""
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Купить павлиньи перья')    # selenium - input
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку')

        self.fail('Закончить тест!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: можно начать свой список для двух и более пользователей по своим url"""
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('row 1')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: row 1')

        first_list_url = self.browser.current_url
        self.assertRegex(first_list_url, '/lists/.+')
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # другой пользователь хочет создать свой список дел
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('row 1', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('row 2')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: row 2')

        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(second_list_url, first_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('row 1', page_text)
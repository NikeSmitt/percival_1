import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self) -> None:
        self.browser = FunctionalTest.get_new_browser()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f'http://{staging_server}'
    
    def tearDown(self) -> None:
        self.browser.quit()
    
    @staticmethod
    def get_new_browser():
        service = ChromeService(executable_path=ChromeDriverManager(version='114.0.5735.90').install())
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        return webdriver.Chrome(service=service, options=options)
    
    def check_list_item_in_table(self, item_text):
        # table = self.browser.find_element(By.ID, 'id_list_table')
        table = WebDriverWait(self.browser, timeout=5).until(lambda x: x.find_element(By.ID, 'id_list_table'))
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(item_text, [row.text for row in rows])
        
    def wait_for(self, fn):
        """Ожидаем элемент"""
        
        element = WebDriverWait(self.browser, timeout=5).until(fn)
        return element

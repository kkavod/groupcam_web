from urlparse import urlparse, urljoin

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BaseLiveServerTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        cls.driver.maximize_window()
        super(BaseLiveServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(BaseLiveServerTestCase, cls).tearDownClass()

    def path_to_url(self, path):
        return urljoin(self.live_server_url, path)

    def get_url(self, path):
        self.driver.get(self.path_to_url(path))
        self.wait_for_page_loaded()

    def get_current_path(self):
        return urlparse(self.driver.current_url).path

    def wait_until(self, waiter, timeout=5, message=''):
        return WebDriverWait(self.driver, timeout).until(waiter, message)

    def wait_until_not(self, waiter, timeout=5, message=''):
        return WebDriverWait(self.driver, timeout).until_not(waiter, message)

    def wait_for_page_loaded(self):
        waiter = lambda driver: driver.find_element_by_tag_name('body')
        return self.wait_until(waiter)

    def wait_for_clickable(self, locator, message=''):
        waiter = expected_conditions.element_to_be_clickable(locator)
        return self.wait_until(waiter, message=message)

    def wait_for_invisible(self, locator, message=''):
        waiter = expected_conditions.invisibility_of_element_located(locator)
        return self.wait_until(waiter, message=message)

    def scroll_to(self, x, y):
        self.driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))

    def scroll_to_top(self):
        self.scroll_to(0, 0)

    def scroll_to_bottom(self):
        self.scroll_to(0, 'document.body.scrollHeight')

    def scroll_to_element(self, element):
        self.scroll_to(element.location['x'], element.location['y'])

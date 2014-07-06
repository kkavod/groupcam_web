from urllib.parse import urlparse, urljoin

import pytest

from django.test import LiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from groupcam_web.tests.middleware import TESTING_FLAGS
from groupcam_web.tests.factories import DEFAULT_PASSWORD


class BaseLiveServerTestCase(LiveServerTestCase):
    @classmethod
    def setup_class(cls):
        cls.driver = WebDriver()
        cls.driver.maximize_window()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @pytest.fixture(autouse=True)
    def set_default_camera(self, default_camera):
        self.default_camera = default_camera

    def go_to(self, path):
        self.driver.get(self.get_url_from_path(path))
        self.wait_for_page_loaded()

    def get_url_from_path(self, path):
        return urljoin(self.live_server_url, path)

    def get_current_path(self):
        return urlparse(self.driver.current_url).path

    def wait_until(self, waiter, message="", timeout=5):
        return WebDriverWait(self.driver, timeout).until(waiter, message)

    def wait_until_not(self, waiter, message="", timeout=5):
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


class BaseAuthenticatedTestCase(BaseLiveServerTestCase):
    @pytest.fixture(autouse=True)
    def set_default_camera(self, default_camera):
        super().set_default_camera(default_camera)
        TESTING_FLAGS['auth_camera'] = default_camera

    def teardown_method(self, method):
        TESTING_FLAGS['auth_camera'] = None

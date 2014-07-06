import json

import httpretty
from django.conf import settings
from selenium.webdriver.common.by import By

from groupcam_web.tests.base import BaseAuthenticatedTestCase


USER_LOCATOR = (By.CSS_SELECTOR, '#js-users-container .js-user')


class TestPresets(BaseAuthenticatedTestCase):
    def setup_method(self, method):
        httpretty.reset()
        self._user_names = ['Aaron', 'Abdul', 'Abdullah', 'Abel', 'Abraham']

    @httpretty.activate
    def test_users_presence(self):
        self._mock_users_api()
        self.go_to('/')
        user_elems = self.driver.find_elements(*USER_LOCATOR)
        user_names = [user_elem.text.strip() for user_elem in user_elems]
        assert user_names == self._user_names, "Incorrect users list"

    def test_users_reload(self):
        pass

    def test_quick_search(self):
        pass

    def _mock_users_api(self):
        users = {
            'users': [{'name': user_name}
                      for user_name in self._user_names],
            'ok': True,
        }
        httpretty.register_uri(httpretty.GET,
                               settings.REST_API_URL + '/users',
                               body=json.dumps(users),
                               content_type='text/json')

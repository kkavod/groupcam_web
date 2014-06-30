from selenium.webdriver.common.by import By
from django.core.urlresolvers import reverse

from groupcam_web.tests.factories import DEFAULT_PASSWORD
from groupcam_web.tests.base import (BaseLiveServerTestCase,
                                     BaseAuthenticatedTestCase)


CAMERA_ID_LOCATOR = (By.NAME, 'username')
PASSWORD_LOCATOR = (By.NAME, 'password')
SUBMIT_LOCATOR = (By.CSS_SELECTOR, 'button[type=submit]')
FIELD_ERROR_LOCATOR = (By.CSS_SELECTOR, '.has-error')
NON_FIELD_ERROR_LOCATOR = (By.CSS_SELECTOR, '.alert-danger')

CAMERA_CTRL_LOCATOR = (By.ID, 'js-camera-control')
LOGOUT_CTRL_LOCATOR = (By.ID, 'js-logout-control')


class TestLogin(BaseLiveServerTestCase):
    def setup_method(self, method):
        self._login_url = reverse('login')

    def test_login_redirect(self):
        self.go_to('/')
        waiter = lambda driver: self.get_current_path() == self._login_url
        error_msg = ("Unauthorized user hasn't been"
                     "redirected to the login page")
        self.wait_until(waiter, error_msg)

    def test_login(self):
        self._try_login(self.default_camera.camera_id, DEFAULT_PASSWORD)
        waiter = lambda driver: self.get_current_path() == '/'
        self.wait_until(waiter, "Login failed")

    def test_invalid_login(self):
        self._try_login('fakeuser', DEFAULT_PASSWORD)
        self._wait_for_login_error(non_field_error=True)

        self._try_login('', DEFAULT_PASSWORD)
        self._wait_for_login_error()

        self._try_login(self.default_camera.camera_id, '')
        self._wait_for_login_error()

        self._try_login('fakeuser', 'fakepassword')
        self._wait_for_login_error(non_field_error=True)

        self._try_login('', 'fakepassword')
        self._wait_for_login_error()

        self._try_login('fakeuser', '')
        self._wait_for_login_error()

        self._try_login('', '')
        self._wait_for_login_error()

    def _try_login(self, login, password):
        self.go_to(self._login_url)
        camera_id_elem = self.driver.find_element(*CAMERA_ID_LOCATOR)
        camera_id_elem.send_keys(login)
        password_elem = self.driver.find_element(*PASSWORD_LOCATOR)
        password_elem.send_keys(password)
        submit_elem = self.driver.find_element(*SUBMIT_LOCATOR)
        submit_elem.click()

    def _wait_for_login_error(self, non_field_error=False):
        locator = (NON_FIELD_ERROR_LOCATOR
                   if non_field_error
                   else FIELD_ERROR_LOCATOR)
        waiter = lambda driver: bool(self.driver.find_elements(*locator))
        self.wait_until(waiter, "No login errors reported")
        assert self.get_current_path() == self._login_url


def create_session_store():
    """ Creates a session storage object. """

    from django.utils.importlib import import_module
    from django.conf import settings
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    store.save()
    return store


class TestLogout(BaseAuthenticatedTestCase):
    def test_logout(self):
        from django.conf import settings
        session_store = create_session_store()
        session_items = session_store
        session_items['uid'] = 1
        session_items.save()
        self.driver.add_cookie({'name': settings.SESSION_COOKIE_NAME, 'value': session_store.session_key})
        self.go_to('/')
        import pdb; pdb.set_trace()

        for locator in (CAMERA_CTRL_LOCATOR, LOGOUT_CTRL_LOCATOR):
            ctrl = self.driver.find_element(*locator)
            ctrl.click()

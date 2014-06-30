from django.core.urlresolvers import reverse

from groupcam_web.tests.base import BaseLiveServerTestCase


class TestAuth(BaseLiveServerTestCase):
    def setup_method(self, method):
        self._login_url = reverse('login')

    def test_login_redirect(self):
        self.go_to('/')
        waiter = lambda driver: self.get_current_path() == self._login_url
        error_msg = ("Unauthorized user hasn't been"
                     "redirected to the login page")
        self.wait_until(waiter, error_msg)

    def test_login(self):
        self.go_to(self._login_url)
        camera_id = self.driver.find_element_by_name('id')
        camera_id.send_keys(self.default_camera.camera_id)
        password = self.driver.find_element_by_name('password')
        password.send_keys(self.default_camera.password)
        submit = self.driver.find_by_css_selector('button[type=submit]')
        submit.click()
        waiter = lambda driver: self.get_current_path() == '/'
        self.wait_until(waiter, "Login failed")

    def test_invalid_login(self):
        pass

    def test_logout(self):
        pass

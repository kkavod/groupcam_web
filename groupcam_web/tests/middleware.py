from django.contrib.auth import authenticate, login

from groupcam_web.tests.factories import DEFAULT_PASSWORD


TESTING_FLAGS = {
    'auth_camera': None,
}


class TestingMiddleware:
    def process_request(self, request):
        default_camera = TESTING_FLAGS.get('auth_camera')
        if default_camera is not None:
            camera = authenticate(
                username=default_camera.camera_id,
                password=DEFAULT_PASSWORD
            )
            login(request, camera)

import os

from groupcam_web.tests.factories import CameraFactory


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "groupcam_web.testing_settings")


def pytest_runtestloop(session):
    default_camera = CameraFactory.create()
    return default_camera

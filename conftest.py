import os

import pytest


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "groupcam_web.testing_settings")


@pytest.fixture()
def default_camera():
    from groupcam_web.tests.factories import CameraFactory
    return CameraFactory.create()

import os


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "groupcam_web.settings")

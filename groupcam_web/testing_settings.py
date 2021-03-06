from groupcam_web.settings import *  # NOQA

TESTING = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': 'test_db.sqlite3',
    }
}
MIDDLEWARE_CLASSES += ('groupcam_web.tests.middleware.TestingMiddleware',)

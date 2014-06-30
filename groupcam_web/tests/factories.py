import factory

from groupcam_web import models


class CameraFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Camera

    camera_id = factory.Sequence(lambda number: 'camera{}'.format(number))
    email = factory.Sequence(lambda number: 'camera{}@kab.info'.format(number))
    nickname = factory.Sequence(lambda number: "Camera {}".format(number))
    title = factory.Sequence(lambda number: 'Title {}'.format(number))
    regexp = factory.Sequence(lambda number: 'some.*regexp{}'.format(number))
    is_staff = False

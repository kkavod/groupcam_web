from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


class CameraManager(BaseUserManager):
    def create_user(self, camera_id, password, **kwargs):
        camera = self.model(camera_id=camera_id, **kwargs)
        camera.set_password(password)
        camera.save(using=self._db)
        return camera

    def create_superuser(self, camera_id, password, **kwargs):
        camera = self.create_user(camera_id, password, **kwargs)
        camera.is_staff = True
        camera.save(using=self._db)
        return camera


class Camera(AbstractBaseUser):
    USERNAME_FIELD = 'camera_id'

    camera_id = models.CharField(_("Camera ID"), max_length=64, unique=True)
    title = models.CharField(_("Title"), max_length=128)
    nickname = models.CharField(_("Nickname"), max_length=128)
    regexp = models.CharField(_("Regular expression"), max_length=128)
    email = models.EmailField(_("E-Mail"))
    is_staff = models.BooleanField(_("Admin status"), default=False)

    objects = CameraManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()

from django.contrib import admin
from django.contrib.auth.models import Group

from groupcam_web.models import Camera


admin.site.register(Camera)
admin.site.unregister(Group)

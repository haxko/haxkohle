from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


admin.site.unregister(Group)
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(Subscription)

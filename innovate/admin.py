from django.contrib import admin
from .models import User, Startup
# Register your models here.
admin.site.register(Startup)
admin.site.register(User)
from django.contrib import admin
from .models import Mytable, History

# Register your models here.

admin.site.register(Mytable)
admin.site.register(History)
from django.contrib import admin

# Register your models here.
from .models import Cart

#add access onto the /admin
admin.site.register(Cart)
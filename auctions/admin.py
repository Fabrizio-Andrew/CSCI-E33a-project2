from django.contrib import admin
from .models import User, listing

# Register your models here.

admin.site.register(listing)
admin.site.register(User)

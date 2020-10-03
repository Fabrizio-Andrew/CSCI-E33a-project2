from django.contrib import admin
from .models import User, Listing

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)

admin.site.register(Listing)
admin.site.register(User, UserAdmin)

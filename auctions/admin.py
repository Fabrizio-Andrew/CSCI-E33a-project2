"""
Registers models to be managed via the Django admin app.
"""

from django.contrib import admin
from .models import User, Listing, Bids, Comments

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)


admin.site.register(Listing)
admin.site.register(User, UserAdmin)
admin.site.register(Bids)
admin.site.register(Comments)

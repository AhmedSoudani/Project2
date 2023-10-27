from django.contrib import admin
from .models import User, listing, bids, comments

# Register your models here.
admin.site.register(User)
admin.site.register(listing)
admin.site.register(bids)
admin.site.register(comments)
from django.contrib import admin
from .models import User, listing

# Register your models here.
admin.site.register(User)
admin.site.register(listing)
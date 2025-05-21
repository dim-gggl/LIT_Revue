from django.contrib import admin
from .models import User, UserFollows, Ticket, Review

admin.site.register(User)
admin.site.register(UserFollows)
admin.site.register(Ticket)
admin.site.register(Review)

# Register your models here.

from django.contrib import admin

from .models import User, Category, Auction_Listing, Bid, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction_Listing)
admin.site.register(Bid)
admin.site.register(Comment)

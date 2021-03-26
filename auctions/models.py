from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"


class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction_Listing', blank=True)

    def __str__(self):
        return f"User: {self.pk} {self.username}"
    pass


class Auction_Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    url_image = models.URLField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="User")
    closed = models.BooleanField()

    def __str__(self):
        return f"Listing: {self.title}"
        # , Description: {self.description}, Starting Bid: {self.starting_bid}, Category: {self.category}"


class Bid(models.Model):
    listing = models.ForeignKey(
        Auction_Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f"{self.user}'s {self.bid} bid on {self.listing}"


class Comment(models.Model):
    comment_title = models.CharField(max_length=64)
    comment = models.TextField()
    listing = models.ForeignKey(
        Auction_Listing, on_delete=models.CASCADE, related_name="comment_listing")
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")

    def __str__(self):
        return f"'{self.comment}' -{self.commenter}"

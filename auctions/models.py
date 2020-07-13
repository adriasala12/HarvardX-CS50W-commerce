from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name="watchlist")

class Listing(models.Model):

    name = models.CharField(max_length=64)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    image_url = models.CharField(max_length=600, default="https://freesvg.org/img/Placeholder.png")
    is_active = models.BooleanField(default=True)

    CATEGORIES = [
        ("1", "Books"),
        ("2", "Business & Industrial"),
        ("3", "Clothing, Shoes & Accessories"),
        ("4", "Collectibles"),
        ("5", "Consumer Electronics"),
        ("6", "Crafts"),
        ("7", "Dolls & Bears"),
        ("8", "Home & Garden"),
        ("9", "Motors"),
        ("10", "Pet Supplies"),
        ("11", "Sporting Goods"),
        ("12", "Sports Mem, Cards & Fan Shop"),
        ("13", "Toys & Hobbies"),
        ("14", "Antiques"),
        ("15", "Computers, Tablets & Networking")
    ]

    category = models.CharField(max_length=2, choices=CATEGORIES)


class Bid(models.Model):

    price = models.DecimalField(max_digits=8, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):

    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    watchlist = models.ManyToManyField('listing', blank=True, related_name="watched_by")

    def __str__(self) :
        return f"{self.username.capitalize()}"

class listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", default=None)
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    isactive = models.BooleanField(default=True)
    image_URL = models.URLField(max_length=200, blank=True, null=True)
    winner = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if not self.creator:
            # Set the creator to the currently logged-in user
            self.creator = User.objects.get(username=self.username)
        super(listing, self).save(*args, **kwargs)

    def __str__(self):
        return f"Title:{self.title} By {self.creator}!"

    
class bids(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_owner")
    title = models.ForeignKey(listing, on_delete=models.CASCADE)
    bid_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Bid by {self.owner} on '{self.title}' at ${self.bid_price}"
    
class comments(models.Model):
    item_id = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="item_id")
    content = models.TextField(max_length=500, blank=False, null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return f"Mr {self.customer} has commented to {self.item_id}!"

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    favourites = models.ManyToManyField("Startup")

class Startup(models.Model):
    name = models.CharField(max_length = 30)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    business_plan = models.FileField()
    founder = models.ForeignKey("User", on_delete=models.CASCADE, related_name="founder")
    members = models.ManyToManyField("User", related_name="members", blank=True)
    description = models.TextField()
    investors = models.ManyToManyField("User", related_name="investments", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "founder": self.sender.email,
            "members": [user.username for user in self.members.all()],
            "investors": [user.username for user in self.investors.all()],
            "name": self.name,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "status": self.status        
        }
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Startup(models.Model):
    name = models.CharField(max_length = 30)
    founder = models.ForeignKey("User", on_delete=models.CASCADE, related_name="founder")
    members = models.ManyToManyField("User", related_name="members", blank=True)
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
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
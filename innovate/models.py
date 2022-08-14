from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"

# Create your models here.
class User(AbstractUser):
    favourites = models.ManyToManyField("Startup")
    profile = models.ImageField(upload_to='images/profiles/', null=True, blank=True)

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
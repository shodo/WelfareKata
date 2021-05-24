import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Type(models.TextChoices):
        BASIC = "Basic", _("Basic")
        PREMIUM = "Premium", _("Premium")
        GOLD = "Gold", _("Gold")

    external_id = models.UUIDField(
        null=False,
        default=uuid.uuid4,
        blank=False,
        unique=True,
    )

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default=None,
    )

    description = models.CharField(
        max_length=400,
        null=False,
        blank=False,
        default=None,
    )

    type = models.TextField(
        max_length=10,
        choices=Type.choices,
        null=False,
        blank=False,
        default=None,
    )

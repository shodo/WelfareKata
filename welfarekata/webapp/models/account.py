import uuid
from django.db import models


class Account(models.Model):
    external_id = models.UUIDField(
        null=False,
        default=uuid.uuid4,
        blank=False,
        unique=True,
    )

    credits = models.IntegerField(
        null=False,
        blank=False,
        default=0,
    )

    employee_external_id = models.UUIDField(
        null=False,
        blank=False,
        unique=True,
    )

    creation_date = models.DateField(
        null=False,
        blank=False,
        auto_now_add=True,
    )

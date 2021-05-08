import uuid

from django.utils import timezone

from welfarekata.webapp.models.product import Product
from welfarekata.webapp.models.account import Account
from django.db import models


class Purchase(models.Model):
    external_id = models.UUIDField(null=False,
                                   default=uuid.uuid4,
                                   blank=False,
                                   unique=True)

    account = models.ForeignKey(Account,
                                related_name="purchases",
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE)

    product = models.ForeignKey(Product,
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE)

    spent_credits = models.IntegerField(null=False, blank=False, default=0)

    creation_date = models.DateTimeField(null=False,
                                         blank=False,
                                         default=timezone.now)

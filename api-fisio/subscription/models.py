from django.db import models


class Subscription(models.Model):
    FREE = 1
    BRONZE = 2
    SILVER = 3
    GOLD = 4
    SUBSCRIPTIONS_TYPES = (
        (FREE, 'Gratis'),
        (BRONZE, 'Bronze'),
        (SILVER, 'Prata'),
        (GOLD, 'Ouro'),
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    type = models.PositiveSmallIntegerField(
        'Subscription',
        choices=SUBSCRIPTIONS_TYPES,
        default=FREE
    )

    def __str__(self):
        return self.type

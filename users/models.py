from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


class Member(User):
    """
    Proxymodel to extend the User class with some functionality to handle Subscriptions
    """
    class Meta:
        proxy: True

    def __get__(self, key):
        subscription_attributes = ['current_membership_fee', 'current_begin_date', 'current_end_date', 'current_membership_number']
        if key in subscription_attributes + ['current_subscription']:
            for subscription in self.subscription_set:
                if subscription.begin_date > timezone.now(): return
                if subscription.end_date < timezone.now(): return
                if key == 'current_subscription':
                    return subscription
                return getattr(subscription, key)
        elif key == 'subscriptions':
            return self.subscription_set
        return super(Member, self).__get(key)

class Subscription(models.Model):
    """
    A subscription is adds additional information to a member
    A member can have multiple subscriptions but only one subscription
    can be active for the current timeframe.
    """
    INTERVAL_CHOICES = ((0, 'daily'), (1, 'weekly'), (2, 'monthly'), (3, 'quarterly'), (4, 'yearly'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    membership_fee = models.DecimalField(max_digits=11, decimal_places=2)
    fee_intervall = models.IntegerField(default=2, choices=INTERVAL_CHOICES)
    begin_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    membership_number = models.IntegerField(blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_initial_user_membership(sender, instance, created, **kwargs):
        if created:
            Subscription.objects.create(
                user=instance,
                membership_fee=settings.DEFAULT_MONTLY_FEE,
                begin_date=timezone.now(),
            )

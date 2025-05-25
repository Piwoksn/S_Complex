from django.db import models
from myapp.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class NairaSubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('Basic', 'Basic - Daily Plan'),
        ('Platinum', 'Platinum - Monthly Plan'),
        ('Bronze', 'Bronze - Quarterly Plan'),
        ('Silver', 'Silver - Biannual Plan'),
        ('Gold', 'Gold - Annual Plan'),
        # Foreign
        ('ForeignBasic', 'Basic - Daily Plan'),
        ('ForeignPlatinum', 'Platinum - Monthly Plan'),
        ('ForeignBronze', 'Bronze - Quarterly Plan'),
        ('ForeignSilver', 'Silver - Biannual Plan'),
        ('ForeignGold', 'Gold - Annual Plan'),
    )
    
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.get_plan_type_display()


class DollarSubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('Basic', 'Basic - Daily Plan'),
        ('Platinum', 'Platinum - Monthly Plan'),
        ('Bronze', 'Bronze - Quarterly Plan'),
        ('Silver', 'Silver - Biannual Plan'),
        ('Gold', 'Gold - Annual Plan'),
    )

    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.get_plan_type_display()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_no = models.CharField(max_length=200, null=True, blank=True)

    naira_plan = models.ForeignKey(
        NairaSubscriptionPlan, on_delete=models.CASCADE, null=True, blank=True)
    dollar_plan = models.ForeignKey(
        DollarSubscriptionPlan, on_delete=models.CASCADE, null=True, blank=True)
    datenow = models.DateTimeField(
        default=timezone.now, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    # Automatically calculate based on the selected plan's duration
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.naira_plan:
            # Calculate end_date based on the selected Naira plan's duration
            if self.naira_plan.plan_type == 'Platinum':
                self.end_date = self.start_date + timezone.timedelta(days=30)
            elif self.naira_plan.plan_type == 'Basic':
                self.end_date = self.start_date + timezone.timedelta(days=1)
            elif self.naira_plan.plan_type == 'Bronze':
                self.end_date = self.start_date + timezone.timedelta(days=90)
            elif self.naira_plan.plan_type == 'Silver':
                self.end_date = self.start_date + timezone.timedelta(days=180)
            elif self.naira_plan.plan_type == 'Gold':
                self.end_date = self.start_date + timezone.timedelta(days=365)
                # Foreign
            elif self.naira_plan.plan_type == 'ForeignPlatinum':
                self.end_date = self.start_date + timezone.timedelta(days=30)
            elif self.naira_plan.plan_type == 'ForeignBasic':
                self.end_date = self.start_date + timezone.timedelta(days=1)
            elif self.naira_plan.plan_type == 'ForeignBronze':
                self.end_date = self.start_date + timezone.timedelta(days=90)
            elif self.naira_plan.plan_type == 'ForeignSilver':
                self.end_date = self.start_date + timezone.timedelta(days=180)
            elif self.naira_plan.plan_type == 'ForeignGold':
                self.end_date = self.start_date + timezone.timedelta(days=365)

        elif self.dollar_plan:
            # Calculate end_date based on the selected Dollar plan's duration
            if self.dollar_plan.plan_type == 'Platinum':
                self.end_date = self.start_date + timezone.timedelta(days=30)
            elif self.dollar_plan.plan_type == 'Basic':
                self.end_date = self.start_date + timezone.timedelta(days=1)
            elif self.dollar_plan.plan_type == 'Bronze':
                self.end_date = self.start_date + timezone.timedelta(days=90)
            elif self.dollar_plan.plan_type == 'Silver':
                self.end_date = self.start_date + timezone.timedelta(days=180)
            elif self.dollar_plan.plan_type == 'Gold':
                self.end_date = self.start_date + timezone.timedelta(days=365)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - Subscription'

    def is_expired(self):
        return self.end_date < timezone.now()

    def renew(self):
        if self.is_expired():
            if self.naira_plan:
                if self.naira_plan.plan_type == 'Platinum':
                    new_end_date = self.end_date + timezone.timedelta(days=30)
                elif self.naira_plan.plan_type == 'Bronze':
                    new_end_date = self.end_date + timezone.timedelta(days=90)
                elif self.naira_plan.plan_type == 'Basic':
                    new_end_date = self.end_date + timezone.timedelta(days=1)
                elif self.naira_plan.plan_type == 'Silver':
                    new_end_date = self.end_date + timezone.timedelta(days=180)
                elif self.naira_plan.plan_type == 'Gold':
                    new_end_date = self.end_date + timezone.timedelta(days=365)
                    # Foreign
                elif self.naira_plan.plan_type == 'ForeignPlatinum':
                    new_end_date = self.end_date + timezone.timedelta(days=30)
                elif self.naira_plan.plan_type == 'ForeignBronze':
                    new_end_date = self.end_date + timezone.timedelta(days=90)
                elif self.naira_plan.plan_type == 'ForeignBasic':
                    new_end_date = self.end_date + timezone.timedelta(days=1)
                elif self.naira_plan.plan_type == 'ForeignSilver':
                    new_end_date = self.end_date + timezone.timedelta(days=180)
                elif self.naira_plan.plan_type == 'ForeignGold':
                    new_end_date = self.end_date + timezone.timedelta(days=365)
            elif self.dollar_plan:
                if self.dollar_plan.plan_type == 'Platinum':
                    new_end_date = self.end_date + timezone.timedelta(days=30)
                elif self.dollar_plan.plan_type == 'Bronze':
                    new_end_date = self.end_date + timezone.timedelta(days=90)
                elif self.dollar_plan.plan_type == 'Silver':
                    new_end_date = self.end_date + timezone.timedelta(days=180)
                elif self.dollar_plan.plan_type == 'Gold':
                    new_end_date = self.end_date + timezone.timedelta(days=365)

            self.end_date = new_end_date
            self.is_active = True
            self.save()

    def cancel(self):
        self.is_active = False
        self.save()

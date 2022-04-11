from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    amount  = models.FloatField()
    title   = models.CharField(max_length=64, null=True, blank=True)


class Expense(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    amount  = models.FloatField()
    title   = models.CharField(max_length=64, null=True, blank=True)


class Debt(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    amount  = models.FloatField()
    title   = models.CharField(max_length=64, null=True, blank=True)

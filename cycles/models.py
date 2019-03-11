from django.contrib.auth.models import User
from django.db import models

class Tenant(models.Model):
    name =  models.CharField(max_length=100)
    income = models.DecimalField(max_digits=9, decimal_places=2)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    deletedOn = models.DateField(default=None, null=True)
    cycle = models.ManyToManyField("Cycle", through='tenantCycle')

    def __str__(self):
      return f'{self.name}'

class Cycle(models.Model):
    name = models.CharField(max_length=100)
    inactive = models.BooleanField(default=None, null=False)
    endDate = models.DateField(default=None)
    split = models.IntegerField(default=0)

    def __str__(self):
      return f'{self.name}'

class tenantCycle(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)

class Bills(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    recurring = models.BooleanField(default=None, null=False)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)

    def __str__(self):
      return f'{self.name}'

class Recurring(models.Model):
    name = models.CharField(max_length=100)
    deletedOn = models.DateField(default=None, null=True)

    def __str__(self):
      return f'{self.name}'


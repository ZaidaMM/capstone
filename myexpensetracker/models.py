from django.db import models

# Create your models here.

class Expense(models.Model):
  item = models.CharField(max_length=200)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  type = models.CharField(max_length=200)
  timestamp = models.DateField(auto_now=True)

  def __str__(self):
    return f"{self.item},  £{self.amount}, {self.type}, {self.timestamp}, id:{self.id}"
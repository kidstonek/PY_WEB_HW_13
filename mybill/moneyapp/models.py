from django.db import models


# Create your models here.

class Category(models.Model):
    cname = models.CharField(max_length=25, unique=True, null=False)

    def __str__(self):
        return self.cname


class Expense(models.Model):
    ename = models.CharField(max_length=25, unique=True, null=False)
    evalue = models.IntegerField()
    category = models.ManyToManyField(Category)
    edate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ename

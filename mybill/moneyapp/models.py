from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    cname = models.CharField(max_length=25, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'cname'], name='category of username')
        ]

    def __str__(self):
        return f"{self.cname}:{self.user_id}"


class Expense(models.Model):
    ename = models.CharField(max_length=25, unique=True, null=False)
    evalue = models.IntegerField()
    category = models.ManyToManyField(Category)
    edate = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ename}:{self.user_id}"

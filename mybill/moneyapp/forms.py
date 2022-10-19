from django.forms import ModelForm
from .models import Category, Expense


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['cname']


class CategoryExpense(ModelForm):
    class Meta:
        model = Expense
        fields = ['ename', 'evalue']
        exclude = ['category']

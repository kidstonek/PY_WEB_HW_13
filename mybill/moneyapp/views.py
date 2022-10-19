from django.shortcuts import render, redirect
from .models import Category, Expense
from .forms import CategoryForm, CategoryExpense
from django.db.models import Sum


# Create your views here.
def main(request):
    category = Category.objects.all()
    return render(request, 'moneyapp/index.html', {'categories': category})


def category(request):
    if request.method == 'POST':
        try:
            form = CategoryForm(request.POST)
            form.save()
            return redirect(to='/')
        except ValueError:
            return render(request, 'moneyapp/category.html',
                          {'form': CategoryForm, 'error': 'Category name field too long'})
    return render(request, 'moneyapp/category.html', {'form': CategoryForm})


# def expenses(request):
#     category = Category.objects.all()
#     if request.method == 'POST':
#         try:
#             form = CategoryExpense(request.POST)
#             category = Category.objects.all()
#             new_expense = form.save()
#             new_expense.category.add('category')
#         except ValueError as err:
#             return render(request, 'moneyapp/expenses.html',
#                           {'form': CategoryExpense, 'error': err, 'categories': category})
#     category = Category.objects.all()
#     return render(request, 'moneyapp/expenses.html', {'categories': category})


def expenses(request):
    if request.method == 'POST':
        ename = request.POST['ename']
        evalue = request.POST['value']
        category = Category.objects.all()[0]
        expens = Expense(ename=ename, evalue=evalue,)
        expens.save()
        expens.category.add(category)
    category = Category.objects.all()
    return render(request, 'moneyapp/expenses.html', {'categories': category})


def stats(request):
    expense = Expense.objects.all()
    sum_ = Expense.objects.aggregate(Sum('evalue'))
    return render(request, 'moneyapp/stats.html', {'expenses': expense, 'sum_': sum_['evalue__sum']})

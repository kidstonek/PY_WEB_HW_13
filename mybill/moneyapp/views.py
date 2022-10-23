from django.shortcuts import render, redirect
from .models import Category, Expense
from .forms import CategoryForm, CategoryExpense
from django.db.models import Sum
from datetime import datetime


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


def expenses(request):
    if request.method == 'POST':
        ename = request.POST['ename']
        evalue = request.POST['value']
        category = Category.objects.all()[0]
        expens = Expense(ename=ename, evalue=evalue, )
        expens.save()
        expens.category.add(category)
    category = Category.objects.all()
    return render(request, 'moneyapp/expenses.html', {'categories': category})


def stats(request):
    if request.method == 'POST':
        first_date = request.POST.get('date_from')
        end_date = request.POST.get('date_for')
        try:
            fd = datetime.strptime(first_date, "%Y-%m-%d")
            ed = datetime.strptime(end_date, "%Y-%m-%d")
        except TypeError:
            ed = datetime.now().date()
        rep = Expense.objects.filter(edate__range=[fd, ed]).aggregate(Sum('evalue'))
        return render(request, 'moneyapp/stats.html', {'first_date': first_date, 'end_date': end_date, 'rep': rep['evalue__sum']})
    else:
        return render(request, 'moneyapp/stats.html', {})

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Category, Expense
from .forms import CategoryForm, CategoryExpense
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
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
        category = request.POST['category']
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
        except ValueError:
            fd = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
            ed = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
        rep = Expense.objects.filter(edate__range=[fd, ed]).aggregate(Sum('evalue'))
        return render(request, 'moneyapp/stats.html', {'first_date': first_date, 'end_date': end_date, 'rep': rep['evalue__sum']})
    else:
        return render(request, 'moneyapp/stats.html', {})


def register_usr(request):
    if request.method == 'GET':
        return render(request, 'moneyapp/register.html', {'form': UserCreationForm()})
    else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    return redirect('main')
                except IntegrityError as err:
                    return render(request, 'moneyapp/register.html',
                                  {'form': UserCreationForm(), 'error': 'Username already exist!'})

            else:
                return render(request, 'moneyapp/register.html',
                              {'form': UserCreationForm(), 'error': 'Password did not match'})

def login_usr(request):
    if request.method == 'GET':
        return render(request, 'moneyapp/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'moneyapp/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password didn\'t match'})
        login(request, user)
        return redirect('main')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('main')
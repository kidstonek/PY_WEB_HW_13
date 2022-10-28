from django.shortcuts import render, redirect
from .models import Category, Expense, User
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
    return render(request, 'moneyapp/index.html', {})


def category(request):
    if request.method == 'POST':
        try:
            form = CategoryForm(request.POST)
            category = form.save(commit=False)
            category.user_id = request.user
            category.save()
            return redirect(to='/')
        except ValueError as rrr:
            return render(request, 'moneyapp/category.html',
                          {'form': CategoryForm, 'error': rrr})
    return render(request, 'moneyapp/category.html', {'form': CategoryForm})


def expenses(request):
    category = Category.objects.filter(user_id=request.user).all()
    if request.method == 'POST':
        try:
            ename = request.POST['ename']
            evalue = request.POST['value']
            category = request.POST['category']
            expens = Expense(ename=ename, evalue=evalue, user_id=request.user)
            expens.save()
            expens.category.add(category)
        except ValueError as rrr:
            return render(request, 'moneyapp/expenses.html', {'categories': category, 'error': rrr})
        except IntegrityError as rrr:
            return render(request, 'moneyapp/expenses.html', {'categories': category, 'error': 'name must be unique'})

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
        rep = Expense.objects.filter(user_id=request.user).filter(edate__range=[fd, ed]).aggregate(Sum('evalue'))
        return render(request, 'moneyapp/stats.html',
                      {'first_date': first_date, 'end_date': end_date, 'rep': rep['evalue__sum']})
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
                return redirect('login_usr')
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

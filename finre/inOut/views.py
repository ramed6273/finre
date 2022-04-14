from django.http import HttpResponse
from django.shortcuts import redirect, render
from inOut.models import Income, Expense, Debt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index_view(request, *arg, **kwargs):
    if request.user.is_anonymous:
        return redirect('/login/')
    else:

        income  = Income.objects.filter(user = request.user.id)
        expense = Expense.objects.filter(user = request.user.id)
        debt    = Debt.objects.filter(user = request.user.id)

        incomeAmount    = 0
        expenseAmount   = 0
        debtAmount      = 0

        for item in income:
            incomeAmount    = incomeAmount  + item.amount
        for item in expense:
            expenseAmount   = expenseAmount + item.amount
        for item in debt:
            debtAmount      = debtAmount    + item.amount
        
        totalWithDebt       = incomeAmount - (expenseAmount + debtAmount)
        total               = incomeAmount - expenseAmount
        print(total)
        print(incomeAmount)

        context = {
            'income'    : incomeAmount,
            'expense'   : expenseAmount,
            'debt'      : debtAmount,
            'totalWD'   : totalWithDebt,
            'total'     : total,
            'user'      : request.user
        }

        return render(request, 'index.html', context)

@csrf_exempt
def add_view(request, types):
    if request.user.is_anonymous:
        raise PermissionError
    else:
        if request.POST:
            user        = request.user
            financial   = types
            thisAmount  = request.POST['amount']
            thisTitle   = request.POST['title']

            if financial    == 'income':
                Income( user    = user, amount = thisAmount, title = thisTitle).save()
            elif financial  == 'expense':
                Expense(user    = user, amount = thisAmount, title = thisTitle).save()
            elif financial  == 'debt':
                Debt(   user    = user, amount = thisAmount, title = thisTitle).save()
            else:
                raise PermissionError

            return redirect('../')
        else:
            raise PermissionError

def edit_view(request, types, id):
    if request.user.is_anonymous:
        raise PermissionError
    else:
        if request.POST:
            newAmount = request.POST['amount']
            newTitle     = request.POST['title']
            user      = request.user
            if types == 'income':
                income = Income.objects.get(id = id, user = user)
                income.title = newTitle
                income.amount = newAmount
                income.save()
                return redirect('/view/income/')
            if types == 'expense':
                expense = Expense.objects.get(id = id, user = user)
                expense.title = newTitle
                expense.amount = newAmount
                expense.save()
                return redirect('/view/expense/')
            if types == 'debt':
                debt = Debt.objects.get(id = id, user = user)
                debt.title = newTitle
                debt.amount = newAmount
                debt.save()
                return redirect('/view/debt/')
        else:
            user = request.user
            if types == 'income':
                income = Income.objects.get(id = id, user = user)
                context = {
                    'income' : income
                }
                return render(request, 'edit.html', context)
            elif types == 'expense':
                expense = Expense.objects.get(id = id, user = user)
                context = {
                    'expense' : expense
                }
                return render(request, 'edit.html', context)
            elif types == 'debt':
                debt = Debt.objects.get(id = id, user = user)
                context = {
                    'debt' : debt
                }
                return render(request, 'edit.html', context)
            else:
                raise PermissionError

def item_view(request, types):
    if request.user.is_anonymous:
        raise PermissionError
    else:
        if types == 'income':
            income = Income.objects.filter(user = request.user.id)
            context = {
                'income' : income
            }
            return render(request, 'detail.html', context)
        elif types == 'expense':
            expense = Expense.objects.filter(user = request.user.id)
            context = {
                'expense' : expense
            }
            return render(request, 'detail.html', context)
        elif types == 'debt':
            debt = Debt.objects.filter(user = request.user.id)
            context = {
                'debt' : debt
            }  
            return render(request, 'detail.html', context)
        else:
            raise PermissionError

def delete_view(request,types, id):
    if request.user.is_anonymous:
        raise PermissionError
    else:
        user = request.user
        if types == 'income':
            income = Income.objects.get(id = id, user = user)
            income.delete()
            return redirect('/view/income')
        elif types == 'expense':
            expense = Expense.objects.get(id = id, user = user)
            expense.delete()
            return redirect('/view/expense')
        elif types == 'debt':
            debt = Debt.objects.get(id = id, user = user)
            debt.delete()
            return redirect('/view/debt')
        else:
            raise PermissionError


def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
    else:
        return render(request, 'sign-in.html')


def logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if  User.objects.filter(username = username).exists():
            return HttpResponse('try another username')
        else:
            if password == password2:
                User.objects.create(username=username, password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('passwords doesnt match')
    else:
        return render(request, 'sign-up.html')
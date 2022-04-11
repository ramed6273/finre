from django.http import HttpResponse
from django.shortcuts import render
from inOut.models import Income, Expense, Debt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

def index_view(request, *arg, **kwargs):
    if request.user.is_anonymous:
        raise PermissionError
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
            'total'     : total
        }

        return render(request, 'index.html', context)

@csrf_exempt
def add_view(request, *args, **kwargs):
    if request.POST:
        user        = User.objects.get(username = 'ramed')
        financial   = request.POST['financial']
        thisAmount  = request.POST['amount']
        thisTitle       = request.POST['title']

        if financial    == 'income':
            Income(user     = user, amount = thisAmount, title = thisTitle).save()
        elif financial  == 'expense':
            Expense(user    = user, amount = thisAmount, title = thisTitle).save()
        elif financial  == 'debt':
            Debt(user       = user, amount = thisAmount, title = thisTitle).save()
        else:
            raise PermissionError

        return HttpResponse('200')
    else:
        raise PermissionError

def item_view(request, types):
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
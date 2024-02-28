import datetime
from datetime import timedelta, date
from django.forms import DecimalField
from django.shortcuts import redirect, render
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm
from django import template

# Create your views here.

def days_ago(n):
  return date.today() - timedelta(n)

def index(request):
  if request.method == "POST":
    item = TransactionForm(request.POST)
    if item.is_valid():
      item.save()
       # Transactions by type
  
  select_item = Transaction.objects.values('type').distinct()

  items = Transaction.objects.all()
  transaction_form = TransactionForm()
  amount_total = items.aggregate(Sum('amount'))

  today_figure = days_ago(1)
  data = Transaction.objects.filter(timestamp__gt=today_figure)
  today_total = data.aggregate(Sum('amount'))

  last_seven_days = days_ago(7)
  data = Transaction.objects.filter(timestamp__gt=last_seven_days)
  seven_day_total = data.aggregate(Sum('amount'))

  last_three_months = days_ago(90)
  data = Transaction.objects.filter(timestamp__gt=last_three_months)
  three_months_total = data.aggregate(Sum('amount'))

  last_year = days_ago(365)
  data = Transaction.objects.filter(timestamp__gt=last_year)
  last_year_total = data.aggregate(Sum('amount'))
  
  # Fetch transactions grouped by category with annotated sum
  transactions_by_category = Transaction.objects.filter().values('category').order_by('category').annotate(Sum('amount'))

  # Calculate Net Income
  total_income = Transaction.objects.filter(category='Income').aggregate(Sum('amount'))
  total_expenses = Transaction.objects.filter(category='Expense').aggregate(Sum('amount'))
  
  net_income = total_income['amount__sum'] - total_expenses['amount__sum']

 

  return render(
        request,
        'myexpensetracker/index.html',
        {
            'transaction_form': transaction_form,
            'items': items,
            'amount_total': amount_total,
            'seven_day_total': seven_day_total,
            'today_total': today_total,
            'three_months_total': three_months_total,
            'last_year_total': last_year_total,
            'transactions_by_category': transactions_by_category,
            'net_income': net_income,
            'select_item':select_item
        
        }
    )



def edit(request,id):
  item = Transaction.objects.get(id=id)
  transaction_form = TransactionForm(instance=item)

  if request.method == "POST":
    item = Transaction.objects.get(id=id)
    form = TransactionForm(request.POST, instance=item)
    if form.is_valid():
      form.save()
      return redirect('index')

  return render(request,'myexpensetracker/edit.html', {'transaction_form':transaction_form})

def delete(request, id):
  if request.method == "POST" and 'delete-btn' in request.POST:
    item = Transaction.objects.get(id=id)
    item.delete()
  return redirect('index')



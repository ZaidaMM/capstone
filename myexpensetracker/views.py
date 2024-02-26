import datetime
from datetime import timedelta, date
from django.shortcuts import redirect, render
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm

# Create your views here.

def days_ago(n):
  return date.today() - timedelta(n)

def index(request):
  if request.method == "POST":
    item = ExpenseForm(request.POST)
    if item.is_valid():
      item.save()

  items = Expense.objects.all()
  expense_form = ExpenseForm()
  amount_total = items.aggregate(Sum('amount'))

  today_figure = days_ago(1)
  data = Expense.objects.filter(timestamp__gt=today_figure)
  today_total = data.aggregate(Sum('amount'))

  last_seven_days = days_ago(7)
  data = Expense.objects.filter(timestamp__gt=last_seven_days)
  seven_day_total = data.aggregate(Sum('amount'))

  last_three_months = days_ago(90)
  data = Expense.objects.filter(timestamp__gt=last_three_months)
  three_months_total = data.aggregate(Sum('amount'))

  last_year = days_ago(365)
  data = Expense.objects.filter(timestamp__gt=last_year)
  last_year_total = data.aggregate(Sum('amount'))
  
  expenses_by_type = Expense.objects.filter().values('type').order_by('type').annotate(Sum('amount'))
  
  return render(request, 'myexpensetracker/index.html', {'expense_form':expense_form, 'items':items, 'amount_total':amount_total, 'seven_day_total':seven_day_total, 'today_total':today_total, 'three_months_total':three_months_total, 'last_year_total':last_year_total, 'expenses_by_type':expenses_by_type})

def edit(request,id):
  item = Expense.objects.get(id=id)
  expense_form = ExpenseForm(instance=item)

  if request.method == "POST":
    item = Expense.objects.get(id=id)
    form = ExpenseForm(request.POST, instance=item)
    if form.is_valid():
      form.save()
      return redirect('index')

  return render(request,'myexpensetracker/edit.html', {'expense_form':expense_form})

def delete(request, id):
  if request.method == "POST" and 'delete-btn' in request.POST:
    item = Expense.objects.get(id=id)
    item.delete()
  return redirect('index')



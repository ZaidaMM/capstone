from django.shortcuts import redirect, render
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm

# Create your views here.
def index(request):
  if request.method == "POST":
    item = ExpenseForm(request.POST)
    if item.is_valid():
      item.save()

  items = Expense.objects.all()
  expense_form = ExpenseForm()
  amount_total = items.aggregate(Sum('amount'))
  
  return render(request, 'myexpensetracker/index.html', {'expense_form':expense_form, 'items':items, 'amount_total':amount_total})

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



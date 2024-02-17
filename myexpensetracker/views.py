from django.shortcuts import render
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
  return render(request, 'myexpensetracker/index.html', {'expense_form':expense_form, 'items':items})
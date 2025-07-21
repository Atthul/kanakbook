from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.contrib import messages
from .models import Transaction, Feedback
from datetime import timedelta
from django.utils import timezone

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        if name and email and message_text:
            Feedback.objects.create(name=name, email=email, message=message_text)
            messages.success(request, "Thank you for your message! We’ll get back to you soon.")
        else:
            messages.error(request, "Please fill out all fields before submitting.")
        return redirect('home')

    return render(request, 'expenses/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'expenses/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')
    return render(request, 'expenses/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            return render(request, 'expenses/login.html', {'error': 'Invalid credentials'})
    return render(request, 'expenses/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Initialize
    cash_income = 0
    cash_expense = 0
    bank_income = 0
    bank_expense = 0
    cash_balance = 0
    bank_balance = 0

    for txn in transactions:
        if txn.transaction_type == 'Income':
            if txn.balance_type == 'Cash':
                cash_income += txn.amount
                cash_balance += txn.amount
            else:
                bank_income += txn.amount
                bank_balance += txn.amount
        elif txn.transaction_type == 'Expense':
            if txn.balance_type == 'Cash':
                cash_expense += txn.amount
                cash_balance -= txn.amount
            else:
                bank_expense += txn.amount
                bank_balance -= txn.amount

    total_income = cash_income + bank_income
    total_expenses = cash_expense + bank_expense
    total_available = cash_balance + bank_balance

    if request.method == 'POST':
        title = request.POST['title']
        amount = float(request.POST['amount'])
        description = request.POST.get('description', '')
        transaction_type = request.POST['transaction_type']
        balance_type = request.POST['balance_type']

        Transaction.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            description=description,
            transaction_type=transaction_type,
            balance_type=balance_type
        )
        messages.success(request, "Transaction added successfully.")
        return redirect('dashboard')

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_available': total_available,
        'cash_balance': cash_balance,
        'bank_balance': bank_balance,
        'cash_income': cash_income,
        'cash_expense': cash_expense,
        'bank_income': bank_income,
        'bank_expense': bank_expense,
    }

    return render(request, 'expenses/dashboard.html', context)


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Transaction, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.description = request.POST.get('description', '')
        expense.transaction_type = request.POST.get('transaction_type', expense.transaction_type)
        expense.balance_type = request.POST.get('balance_type', expense.balance_type)
        expense.save()
        messages.success(request, "Transaction updated successfully.")
        return redirect('dashboard')
    return render(request, 'expenses/edit_expense.html', {'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Transaction, id=expense_id, user=request.user)
    expense.delete()
    messages.success(request, "Transaction deleted successfully.")
    return redirect('dashboard')

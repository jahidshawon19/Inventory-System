from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Issue,Return
from .forms import ProductForm, IssueForm, ReturnForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
import csv
from django.http import HttpResponse



@login_required
def dashboard(request):
    products = Product.objects.all()
    total_products = products.count()
    total_stock = sum(p.quantity for p in products)

    today = now().date()
    issues_today = Issue.objects.filter(issued_date__date=today)
    total_issued_today = sum(i.issued_quantity for i in issues_today)

    low_stock = Product.objects.filter(quantity__lte=5)

    recent_issues = Issue.objects.select_related('product').order_by('-issued_date')[:5]
    recent_returns = Return.objects.select_related('product').order_by('-return_date')[:5]

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'total_issued_today': total_issued_today,
        'low_stock': low_stock,
        'recent_issues': recent_issues,
        'recent_returns': recent_returns
    }
    return render(request, 'products/dashboard.html', context)



# products views here 
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})



@login_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})



#issue  product
@login_required
def issue_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = IssueForm(request.POST or None)
    error = None

    if form.is_valid():
        issue_qty = form.cleaned_data['issued_quantity']

        if issue_qty > product.quantity:
            error = "Issued quantity cannot be greater than available stock."
        else:
            product.quantity -= issue_qty
            product.save()   # updates total_price automatically

            issue = form.save(commit=False)
            issue.product = product
            issue.save()

            return redirect('product_list')

    return render(request, 'products/issue_product.html', {
        'product': product,
        'form': form,
        'error': error
    })

@login_required
def issue_history(request):
    issues = Issue.objects.select_related('product').order_by('-issued_date')
    return render(request, 'products/issue_history.html', {'issues': issues})



# Return Product 
@login_required
def return_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ReturnForm(request.POST or None)

    if form.is_valid():
        return_qty = form.cleaned_data['return_quantity']
        product.quantity += return_qty
        product.save()

        ret = form.save(commit=False)
        ret.product = product
        ret.save()

        return redirect('product_list')

    return render(request, 'products/return_product.html', {
        'product': product,
        'form': form
    })

@login_required
def daily_issue_report(request):
    today = now().date()
    issues = Issue.objects.filter(issued_date__date=today)

    total_issued = sum(i.issued_quantity for i in issues)

    return render(request, 'products/daily_issue_report.html', {
        'issues': issues,
        'total_issued': total_issued,
        'today': today
    })

# stock alert 
@login_required
def stock_alerts(request):
    low_stock_products = Product.objects.filter(quantity__lte=5)
    return render(request, 'products/stock_alerts.html', {
        'products': low_stock_products
    })







# =========================
# Daily Sales Report
# =========================
@login_required
def daily_sales_report(request):
    today = now().date()
    issues_today = Issue.objects.select_related('product').filter(issued_date__date=today)

    # Pre-calculate totals for template
    issue_data = []
    total_qty = 0
    total_sales = 0

    for i in issues_today:
        total = i.issued_quantity * i.product.unit_price
        total_qty += i.issued_quantity
        total_sales += total
        issue_data.append({
            'product': i.product,
            'quantity': i.issued_quantity,
            'unit_price': i.product.unit_price,
            'total': total,
            'time': i.issued_date.time(),
        })

    context = {
        'issue_data': issue_data,
        'total_qty': total_qty,
        'total_sales': total_sales,
        'date': today,
    }
    return render(request, 'products/daily_sales_report.html', context)


# =========================
# Monthly Sales Report
# =========================
@login_required
def monthly_sales_report(request):
    # Get selected month from URL (?month=YYYY-MM)
    selected_month = request.GET.get('month')

    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))

            issues = Issue.objects.filter(
                issued_date__year=year,
                issued_date__month=month
            )

            display_month = datetime(year, month, 1).strftime("%B %Y")

        except ValueError:
            # If invalid month format, fallback to current month
            today = now()
            issues = Issue.objects.filter(
                issued_date__year=today.year,
                issued_date__month=today.month
            )
            display_month = today.strftime("%B %Y")
            selected_month = f"{today.year}-{today.month:02d}"

    else:
        # Default: current month
        today = now()
        issues = Issue.objects.filter(
            issued_date__year=today.year,
            issued_date__month=today.month
        )

        display_month = today.strftime("%B %Y")
        selected_month = f"{today.year}-{today.month:02d}"

    issue_data = []
    total_sales = 0
    total_qty = 0

    for i in issues.select_related('product'):
        total = i.issued_quantity * i.product.unit_price

        issue_data.append({
            'product': i.product,
            'quantity': i.issued_quantity,
            'unit_price': i.product.unit_price,
            'total': total,
            'date': i.issued_date.date(),
            'time': i.issued_date.time(),
        })

        total_sales += total
        total_qty += i.issued_quantity

    context = {
        'issue_data': issue_data,
        'total_sales': total_sales,
        'total_qty': total_qty,
        'month': display_month,
        'selected_month': selected_month,
    }

    return render(request, 'products/monthly_sales_report.html', context)

def export_daily_sales_csv(request):
    today = now().date()

    issues = Issue.objects.filter(
        issued_date__date=today
    ).select_related('product')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="daily_sales.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'SL', 'Product', 'Quantity', 'Unit Price', 'Total', 'Time'
    ])

    total_sales = 0

    for idx, i in enumerate(issues, 1):
        total = i.issued_quantity * i.product.unit_price
        total_sales += total

        writer.writerow([
            idx,
            i.product.name,
            i.issued_quantity,
            i.product.unit_price,
            total,
            i.issued_date.strftime("%H:%M")
        ])

    writer.writerow([])
    writer.writerow(['', '', '', 'Total Sales:', total_sales])

    return response

def export_monthly_sales_csv(request):
    import csv
    from django.utils.timezone import now

    selected_month = request.GET.get('month')

    if selected_month:
        year, month = map(int, selected_month.split('-'))
    else:
        today = now()
        year, month = today.year, today.month

    issues = Issue.objects.filter(
        issued_date__year=year,
        issued_date__month=month
    ).select_related('product')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="monthly_sales.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'SL','Product','Quantity','Unit Price','Total','Date','Time'
    ])

    total_sales = 0

    for idx, i in enumerate(issues, 1):
        total = i.issued_quantity * i.product.unit_price
        total_sales += total

        writer.writerow([
            idx,
            i.product.name,
            i.issued_quantity,
            i.product.unit_price,
            total,
            i.issued_date.strftime("%Y-%m-%d"),
            i.issued_date.strftime("%H:%M")
        ])

    writer.writerow([])
    writer.writerow(['', '', '', '', 'Total Sales:', total_sales])

    return response

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('update/<int:id>/', views.product_update, name='product_update'),
    path('delete/<int:id>/', views.product_delete, name='product_delete'),



    #issue product 
    path('issue/<int:id>/', views.issue_product, name='issue_product'),
    path('issues/', views.issue_history, name='issue_history'),
    path('return/<int:id>/', views.return_product, name='return_product'),
    path('stock-alerts/', views.stock_alerts, name='stock_alerts'),
    path('daily-report/', views.daily_issue_report, name='daily_issue_report'),
    path('sales/daily/', views.daily_sales_report, name='daily_sales_report'),
    path('sales/monthly/', views.monthly_sales_report, name='monthly_sales_report'),

    #authentication
    path('login/', LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),



    path('export/daily-csv/', views.export_daily_sales_csv, name='export_daily_sales_csv'),
    path('export/monthly-csv/', views.export_monthly_sales_csv, name='export_monthly_sales_csv'),

]



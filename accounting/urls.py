from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.accounting_index, name='index'),
    path('reports/income-statement/', views.income_statement, name='income_statement'),
    path('reports/balance-sheet/', views.balance_sheet, name='balance_sheet'),
    # Add more accounting URLs here as needed
]
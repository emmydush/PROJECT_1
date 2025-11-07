from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    path('', views.SuperAdminDashboardView.as_view(), name='dashboard'),
    path('businesses/', views.BusinessManagementView.as_view(), name='business_management'),
    path('users/', views.UserManagementView.as_view(), name='user_management'),
    path('subscriptions/', views.SubscriptionManagementView.as_view(), name='subscription_management'),
    path('logs/', views.SystemLogsView.as_view(), name='system_logs'),
    path('user-activity-logs/', views.UserActivityLogsView.as_view(), name='user_activity_logs'),
    path('communication/', views.CommunicationCenterView.as_view(), name='communication_center'),
    path('api-monitoring/', views.APIMonitoringView.as_view(), name='api_monitoring'),
    path('system-monitoring/', views.SystemMonitoringView.as_view(), name='system_monitoring'),
    path('financial-dashboard/', views.FinancialDashboardView.as_view(), name='financial_dashboard'),
    path('export-financial-report/', views.export_financial_report, name='export_financial_report'),
    
    # Tenant account management URLs
    path('branches/', views.branch_list_view, name='branch_list'),
    path('branches/create/', views.branch_create_view, name='branch_create'),
    path('branches/<int:branch_id>/update/', views.branch_update_view, name='branch_update'),
    path('branches/<int:branch_id>/delete/', views.branch_delete_view, name='branch_delete'),
    path('branches/<int:branch_id>/switch/', views.switch_branch_view, name='branch_switch'),
    path('branches/reports/', views.branch_reports_view, name='branch_reports'),
    path('business/update/', views.business_update_view, name='business_update'),
    path('business/deactivate/', views.business_deactivate_view, name='business_deactivate'),
]
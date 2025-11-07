from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.create_user_view, name='create_user'),
    path('users/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('users/deactivate/<int:user_id>/', views.deactivate_user_view, name='deactivate_user'),
    path('users/activate/<int:user_id>/', views.activate_user_view, name='activate_user'),
    path('users/reset-password/<int:user_id>/', views.reset_user_password_view, name='reset_user_password'),
    path('business-details/', views.business_details_view, name='business_details'),
]
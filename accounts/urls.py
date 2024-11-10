# ganzithon/accounts/urls.py
from django.urls import path
from .views import CustomRegisterView, CustomLoginView, CustomLogoutView, delete_user, create_user_info

app_name = 'accounts'

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('delete/', delete_user, name='delete_user'),
    path('info/', create_user_info, name='create_user_info'),
]

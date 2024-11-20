# ganzithon/accounts/urls.py
from django.urls import path
from .views import CustomRegisterView, CustomLoginView, CustomLogoutView, delete_user, user_info

app_name = 'accounts'

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='signup'),  # 회원가입
    path('login/', CustomLoginView.as_view(), name='login'),  # 로그인
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # 로그아웃
    path('delete/', delete_user, name='delete_user'),  # 회원탈퇴
    path('info/', user_info, name='user_info'),  # 유저 정보 조회, 생성 및 수정
]

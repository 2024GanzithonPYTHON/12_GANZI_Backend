# ganzithon/purchase/urls.py
from django.urls import path
from .views import PurchasePostView, ApplyToPurchaseView,UserApplicationsView

app_name = 'purchase'

urlpatterns = [
    path('', PurchasePostView.as_view(), name='purchase_post_list_create'),  # 전체 게시글 조회 및 생성
    path('<int:pk>/', PurchasePostView.as_view(), name='purchase_post_detail'),  # 특정 게시글 조회, 수정, 삭제
    path('<int:pk>/apply/', ApplyToPurchaseView.as_view(), name='apply_to_post'),  # 공동 구매 신청
    path('applications/', UserApplicationsView.as_view(), name='user-applications'),  # 사용자의 신청 내역 조회
]
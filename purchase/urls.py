# ganzithon/purchase/urls.py
from django.urls import path
from .views import PurchasePostView

app_name = 'purchase'

urlpatterns = [
    path('', PurchasePostView.as_view(), name='purchase_post'), # 공동 구매 게시글 생성
]

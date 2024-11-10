from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    # path('', blog_list),
    path('', BlogList.as_view()),
    # path('<int:pk>/', blog_detail),
    path('<int:pk>/', BlogDetail.as_view()),
]
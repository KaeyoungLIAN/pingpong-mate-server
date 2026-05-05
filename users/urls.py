from django.urls import path
from . import views

urlpatterns = [
    # 微信登录（无需认证）
    path('login/', views.WeChatLoginView.as_view(), name='wechat-login'),
    # 个人资料（需认证）
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    # 查看其他用户
    path('<int:user_id>/', views.UserDetailView.as_view(), name='user-detail'),
]

"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # DRF 自带的登录/注销视图（仅用于浏览式 API）
    path('api-auth/', include('rest_framework.urls')),
    # 各应用路由
    path('api/users/', include('users.urls')),
    path('api/matches/', include('matches.urls')),
]

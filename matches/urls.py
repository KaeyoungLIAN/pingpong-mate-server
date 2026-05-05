from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 使用 DefaultRouter 注册 MatchViewSet
router = DefaultRouter()
router.register(r'', views.MatchViewSet, basename='match')

urlpatterns = [
    # 报名/取消报名
    path('<int:match_id>/apply/', views.MatchApplyView.as_view(), name='match-apply'),
    path('<int:match_id>/cancel-apply/', views.CancelMatchApplyView.as_view(), name='match-cancel-apply'),
    # 我发起的和报名的赛事
    path('my/', views.MyMatchesView.as_view(), name='match-my'),
    # ViewSet 路由（list / create / retrieve / update / destroy）
    path('', include(router.urls)),
]

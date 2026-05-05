from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import (
    WeChatLoginSerializer,
    UserProfileSerializer,
    UserSimpleSerializer,
)


# ---------------------------------------------------------------------------
# 微信登录（无需认证）
# ---------------------------------------------------------------------------
class WeChatLoginView(APIView):
    """
    登录接口
    POST /api/users/login/
    支持两种模式：
    - { "code": "xxx" }  → 微信登录 mock（已有逻辑）
    - { "user_id": "A" } → Demo 选择用户登录
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    # Demo 用户预设资料
    DEMO_USERS = {
        'A': {
            'nickname': '小张',
            'gender': 'male',
            'age': 28,
            'skill_level': 3,
            'district': '朝阳区',
            'paddle_type': '横板',
            'rubber_type': '反胶',
            'bio': '周末约球，欢迎来朝阳',
        },
        'B': {
            'nickname': '小李',
            'gender': 'male',
            'age': 22,
            'skill_level': 1,
            'district': '海淀区',
            'paddle_type': '直板',
            'rubber_type': '正胶',
            'bio': '刚学乒乓球，求带',
        },
        'C': {
            'nickname': '小王',
            'gender': 'female',
            'age': 35,
            'skill_level': 5,
            'district': '东城区',
            'paddle_type': '横板',
            'rubber_type': '反胶',
            'bio': '专业退役，欢迎切磋',
        },
    }

    def post(self, request):
        serializer = WeChatLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # 模式1：Demo 用户选择登录
        if data.get('user_id'):
            user_id = data['user_id'].upper()
            if user_id not in self.DEMO_USERS:
                return Response(
                    {'message': f'无效的用户标识: {user_id}，可选 A/B/C'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            preset = self.DEMO_USERS[user_id]
            openid = f'demo_{user_id}'
            user, created = User.objects.get_or_create(
                wechat_openid=openid,
                defaults={
                    'nickname': preset['nickname'],
                    'gender': preset['gender'],
                    'age': preset['age'],
                    'skill_level': preset['skill_level'],
                    'district': preset['district'],
                    'paddle_type': preset['paddle_type'],
                    'rubber_type': preset['rubber_type'],
                    'bio': preset['bio'],
                    'is_profile_complete': True,
                },
            )

        # 模式2：微信登录 mock（已有逻辑）
        else:
            code = data['code']
            import hashlib
            openid = 'mock_' + hashlib.md5(code.encode()).hexdigest()[:12]
            user, created = User.objects.get_or_create(
                wechat_openid=openid,
                defaults={'nickname': f'球友_{openid[-4:]}'}
            )

        # 获取或创建 DRF Token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data,
            'is_new': created,
        }, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# 个人资料（获取/更新）
# ---------------------------------------------------------------------------
class UserProfileView(RetrieveUpdateAPIView):
    """
    当前用户个人资料
    GET  /api/users/profile/  → 获取当前用户资料
    PUT  /api/users/profile/  → 更新当前用户资料
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        """返回当前登录用户"""
        return self.request.user


# ---------------------------------------------------------------------------
# 查看其他用户基本信息
# ---------------------------------------------------------------------------
class UserDetailView(RetrieveAPIView):
    """
    查看其他用户基本信息
    GET /api/users/<id>/
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSimpleSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'


# ---------------------------------------------------------------------------
# 退出登录
# ---------------------------------------------------------------------------
class LogoutView(APIView):
    """
    退出登录，删除当前用户的 Token
    POST /api/users/logout/
    DELETE /api/users/logout/
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self._logout(request)

    def delete(self, request):
        return self._logout(request)

    def _logout(self, request):
        request.user.auth_token.delete()
        return Response({'message': '已退出登录'}, status=status.HTTP_200_OK)

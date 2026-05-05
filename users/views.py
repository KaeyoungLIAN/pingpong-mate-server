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
    微信登录接口
    POST /api/users/login/
    接收 {code}，mock 微信登录，返回 token 和用户信息
    """
    authentication_classes = []       # 登录接口不要求认证
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WeChatLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        # Mock 微信登录：code 映射固定 openid
        mock_openid_map = {
            'test': 'mock_openid_001',
            'test2': 'mock_openid_002',
            'test3': 'mock_openid_003',
        }
        openid = mock_openid_map.get(code)
        if not openid:
            return Response(
                {'error': '无效的登录凭证'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 查询或创建用户
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

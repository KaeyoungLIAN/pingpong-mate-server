from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Match, MatchApplication
from .serializers import (
    MatchListSerializer, MatchDetailSerializer, MatchCreateSerializer,
    MatchApplicationSerializer,
)


class CancelMatchApplyView(APIView):
    """取消自己的报名"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, match_id):
        match = get_object_or_404(Match, pk=match_id)

        application = get_object_or_404(
            MatchApplication,
            match=match,
            applicant=request.user,
        )

        application.status = MatchApplication.Status.CANCELLED
        application.save()

        return Response(
            {'detail': '报名已取消'},
            status=status.HTTP_200_OK,
        )


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('date', 'time_start')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return MatchCreateSerializer
        if self.action == 'retrieve':
            return MatchDetailSerializer
        return MatchListSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MatchApplyView(APIView):
    """报名/申请参加赛事"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, match_id):
        match = get_object_or_404(Match, pk=match_id)

        # 不能报名自己的约球
        if match.creator == request.user:
            return Response(
                {'detail': '不能报名自己创建的约球'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 检查赛事状态
        if match.status != Match.Status.OPEN:
            return Response(
                {'detail': f'赛事当前状态为「{match.get_status_display()}」，无法报名'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 检查是否已满员
        active_count = match.applications.filter(
            status__in=[MatchApplication.Status.PENDING, MatchApplication.Status.ACCEPTED]
        ).count()
        if active_count >= match.max_players:
            return Response(
                {'detail': '该约球已满员'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 检查是否重复报名
        if MatchApplication.objects.filter(match=match, applicant=request.user).exists():
            return Response(
                {'detail': '你已经报过名了'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 创建报名记录
        application = MatchApplication.objects.create(
            match=match,
            applicant=request.user,
            status=MatchApplication.Status.PENDING,
        )

        serializer = MatchApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyMatchesView(APIView):
    """获取我的约球列表：我发起的 + 我报名的"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        created_matches = Match.objects.filter(creator=request.user).order_by('-date', 'time_start')
        applied_ids = MatchApplication.objects.filter(
            applicant=request.user
        ).exclude(
            status=MatchApplication.Status.CANCELLED
        ).values_list('match_id', flat=True)
        applied_matches = Match.objects.filter(id__in=applied_ids).order_by('-date', 'time_start')

        creator_serializer = MatchListSerializer(created_matches, many=True, context={'request': request})
        applied_serializer = MatchListSerializer(applied_matches, many=True, context={'request': request})

        return Response({
            'created': creator_serializer.data,
            'applied': applied_serializer.data,
        })

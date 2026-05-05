from rest_framework import serializers
from users.serializers import UserSimpleSerializer
from .models import Match, MatchApplication


class MatchListSerializer(serializers.ModelSerializer):
    """赛事列表序列化器：包含创建者信息、报名人数"""
    creator = UserSimpleSerializer(read_only=True)
    applicant_count = serializers.SerializerMethodField()
    vacancies = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'id', 'creator', 'sport_type', 'date', 'time_start', 'time_end',
            'district', 'notes', 'max_players', 'skill_level_required',
            'status', 'applicant_count', 'vacancies', 'created_at',
        ]

    def get_applicant_count(self, obj):
        """返回当前有效报名人数（待确认+已通过）"""
        return obj.applications.filter(
            status__in=[MatchApplication.Status.PENDING, MatchApplication.Status.ACCEPTED]
        ).count()

    def get_vacancies(self, obj):
        """返回缺人数量"""
        count = self.get_applicant_count(obj)
        return max(0, obj.max_players - count)


class MatchDetailSerializer(serializers.ModelSerializer):
    """赛事详情序列化器：包含所有报名人信息"""
    creator = UserSimpleSerializer(read_only=True)
    applicants = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'id', 'creator', 'sport_type', 'date', 'time_start', 'time_end',
            'district', 'notes', 'max_players', 'skill_level_required',
            'status', 'applicants', 'created_at', 'updated_at',
        ]

    def get_applicants(self, obj):
        """返回报名人列表（包含状态）"""
        applications = obj.applications.select_related('applicant').all()
        return [
            {
                'user': UserSimpleSerializer(app.applicant).data,
                'status': app.status,
                'created_at': app.created_at,
            }
            for app in applications
        ]


class MatchCreateSerializer(serializers.ModelSerializer):
    """创建赛事序列化器"""

    class Meta:
        model = Match
        fields = [
            'id', 'date', 'time_start', 'time_end', 'district',
            'notes', 'max_players', 'skill_level_required',
        ]

    def validate_max_players(self, value):
        if value < 2:
            raise serializers.ValidationError('至少需要2人才能开球')
        if value > 50:
            raise serializers.ValidationError('最大参与人数不能超过50')
        return value

    def validate_notes(self, value):
        if len(value) > 100:
            raise serializers.ValidationError('备注不能超过100字')
        return value

class MatchApplicationSerializer(serializers.ModelSerializer):
    """报名序列化器"""
    applicant = UserSimpleSerializer(read_only=True)

    class Meta:
        model = MatchApplication
        fields = ['id', 'match', 'applicant', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'match', 'applicant', 'status', 'created_at', 'updated_at']

from rest_framework import serializers
from .models import User


class WeChatLoginSerializer(serializers.Serializer):
    """微信登录序列化器：接收前端传来的 code"""
    code = serializers.CharField(help_text='微信登录凭证 code')

    def validate_code(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('code 不能为空')
        return value.strip()


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器（完整信息）：创建/更新资料时校验必填字段"""

    class Meta:
        model = User
        fields = [
            'id', 'nickname', 'avatar', 'gender', 'age', 'skill_level',
            'district', 'paddle_type', 'rubber_type', 'bio',
            'is_profile_complete', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'is_profile_complete', 'created_at', 'updated_at']

    def validate_nickname(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('昵称不能为空')
        if len(value) > 50:
            raise serializers.ValidationError('昵称不能超过50个字符')
        return value.strip()

    def validate_age(self, value):
        if value is not None and (value < 0 or value > 150):
            raise serializers.ValidationError('年龄必须在0-150之间')
        return value

    def validate_bio(self, value):
        if len(value) > 50:
            raise serializers.ValidationError('自我介绍不能超过50个字符')
        return value

    def validate_gender(self, value):
        if value not in dict(User.Gender.choices):
            raise serializers.ValidationError(f'无效的性别选项，可选：{dict(User.Gender.choices)}')
        return value

    def validate_skill_level(self, value):
        if value not in dict(User.SkillLevel.choices):
            raise serializers.ValidationError(f'无效的水平等级，可选：{dict(User.SkillLevel.choices)}')
        return value

    def validate_paddle_type(self, value):
        if value not in dict(User.PaddleType.choices):
            raise serializers.ValidationError(f'无效的球板类型，可选：{dict(User.PaddleType.choices)}')
        return value

    def validate_rubber_type(self, value):
        if value not in dict(User.RubberType.choices):
            raise serializers.ValidationError(f'无效的胶皮类型，可选：{dict(User.RubberType.choices)}')
        return value

    def create(self, validated_data):
        """创建用户时自动标记资料为完善"""
        instance = super().create(validated_data)
        instance.is_profile_complete = True
        instance.save(update_fields=['is_profile_complete'])
        return instance

    def update(self, instance, validated_data):
        """更新资料后自动检查并标记是否完善"""
        instance = super().update(instance, validated_data)
        # 检查所有必填字段是否都已填写
        required_fields = ['nickname', 'gender', 'age', 'skill_level', 'district']
        if all(getattr(instance, f, None) for f in required_fields):
            instance.is_profile_complete = True
        else:
            instance.is_profile_complete = False
        instance.save()
        return instance


class UserSimpleSerializer(serializers.ModelSerializer):
    """简化版用户信息：列表/他人资料场景使用"""

    class Meta:
        model = User
        fields = ['id', 'nickname', 'avatar', 'skill_level', 'district']

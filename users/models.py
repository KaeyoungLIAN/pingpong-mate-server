from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """自定义用户模型，基于微信登录"""

    # 性别选项
    class Gender(models.TextChoices):
        MALE = 'male', '男'
        FEMALE = 'female', '女'

    # 水平等级选项（1-5）
    class SkillLevel(models.IntegerChoices):
        BEGINNER = 1, '初学者'
        ELEMENTARY = 2, '初级'
        INTERMEDIATE = 3, '中级'
        ADVANCED = 4, '高级'
        EXPERT = 5, '专业级'

    # 球板类型
    class PaddleType(models.TextChoices):
        SHAKEHAND = '横板', '横板'
        PENHOLD = '直板', '直板'
        JAPANESE_PENHOLD = '日直', '日直'
        UNUSUAL = '异形', '异形'

    # 胶皮类型
    class RubberType(models.TextChoices):
        SMOOTH = '反胶', '反胶'
        PIMPLES_OUT = '正胶', '正胶'
        LONG_PIMPLES = '长胶', '长胶'
        ANTI = '生胶', '生胶'

    # 微信 openid，唯一标识
    wechat_openid = models.CharField('微信 openid', max_length=100, unique=True)
    gender = models.CharField('性别', max_length=10, choices=Gender.choices, null=True, blank=True)
    age = models.IntegerField('年龄', null=True, blank=True)
    skill_level = models.IntegerField('水平等级', choices=SkillLevel.choices, null=True, blank=True)
    district = models.CharField('所在区', max_length=50, default='')
    paddle_type = models.CharField('球板类型', max_length=10, choices=PaddleType.choices, null=True, blank=True)
    rubber_type = models.CharField('胶皮类型', max_length=10, choices=RubberType.choices, null=True, blank=True)
    bio = models.CharField('自我介绍', max_length=50, blank=True, default='')
    avatar = models.URLField('头像 URL', blank=True, default='')
    nickname = models.CharField('昵称', max_length=50, default='')
    is_profile_complete = models.BooleanField('资料是否完善', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    # 不强制使用 Django 默认的 username/email/password
    username = None  # 去掉 username 字段，使用 wechat_openid 作为唯一标识
    first_name = None
    last_name = None
    email = None

    USERNAME_FIELD = 'wechat_openid'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']

    def __str__(self):
        return self.nickname or self.wechat_openid

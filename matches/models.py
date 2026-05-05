from django.db import models
from django.conf import settings


class Match(models.Model):
    """赛事/约球模型"""

    class SkillLevel(models.IntegerChoices):
        BEGINNER = 1, '初学者'
        ELEMENTARY = 2, '初级'
        INTERMEDIATE = 3, '中级'
        ADVANCED = 4, '高级'
        EXPERT = 5, '专业级'

    class Status(models.TextChoices):
        OPEN = 'open', '开放报名'
        FULL = 'full', '已满员'
        CANCELLED = 'cancelled', '已取消'
        COMPLETED = 'completed', '已完成'

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_matches',
        verbose_name='创建者',
    )
    sport_type = models.CharField('运动类型', max_length=20, default='table_tennis')
    date = models.DateField('日期')
    time_start = models.TimeField('开始时间')
    time_end = models.TimeField('结束时间')
    district = models.CharField('所在区', max_length=50)
    notes = models.TextField('备注', max_length=100, blank=True, default='')
    max_players = models.IntegerField('最大参与人数', default=4)
    skill_level_required = models.IntegerField('水平要求', choices=SkillLevel.choices, null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '赛事'
        verbose_name_plural = '赛事'
        ordering = ['-date', 'time_start']

    def __str__(self):
        return f'{self.date} {self.district} - {self.get_status_display()}'


class MatchApplication(models.Model):
    """报名模型"""

    class Status(models.TextChoices):
        PENDING = 'pending', '待确认'
        ACCEPTED = 'accepted', '已通过'
        REJECTED = 'rejected', '已拒绝'
        CANCELLED = 'cancelled', '已取消'

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='赛事',
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='match_applications',
        verbose_name='报名人',
    )
    status = models.CharField('状态', max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField('报名时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '报名记录'
        verbose_name_plural = '报名记录'
        unique_together = ('match', 'applicant')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.applicant.nickname} -> {self.match}'

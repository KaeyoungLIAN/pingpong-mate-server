from django.db import models


class Venue(models.Model):
    """球馆模型（MVP 阶段暂不启用，仅预留表结构）"""

    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'

    name = models.CharField('球馆名称', max_length=100)
    address = models.CharField('地址', max_length=200)
    phone = models.CharField('联系电话', max_length=20, blank=True, default='')
    district = models.CharField('所在区', max_length=50)
    status = models.CharField('状态', max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '球馆'
        verbose_name_plural = '球馆'
        ordering = ['name']

    def __str__(self):
        return self.name

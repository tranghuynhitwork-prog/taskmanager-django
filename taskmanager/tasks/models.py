from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Thấp', 'Thấp'),
        ('Trung bình', 'Trung bình'),
        ('Cao', 'Cao'),
    ]

    title = models.CharField('Tiêu đề', max_length=200)
    description = models.TextField('Mô tả', blank=True)
    due_date = models.DateField('Hạn hoàn thành')
    priority = models.CharField(
        'Mức độ ưu tiên', max_length=20,
        choices=PRIORITY_CHOICES, default='Trung bình',
    )
    is_completed = models.BooleanField('Đã hoàn thành', default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='tasks', verbose_name='Chủ sở hữu',
    )
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)

    class Meta:
        verbose_name = 'Công việc'
        verbose_name_plural = 'Công việc'

    def __str__(self):
        return self.title

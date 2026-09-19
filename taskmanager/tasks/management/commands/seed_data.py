from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from tasks.models import Task


class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu: 1 admin, 2 người dùng và các công việc mẫu'

    def handle(self, *args, **options):
        today = timezone.localdate()

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True,
                      'email': 'admin@example.com'},
        )
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('admin123')
        admin.save()

        users = {}
        for name in ('nguyenvana', 'tranthib'):
            user, _ = User.objects.get_or_create(username=name)
            user.set_password('Test@12345')
            user.save()
            users[name] = user

        data = {
            'nguyenvana': [
                ('Làm bài thực hành Django', 'Hoàn thành Bài thực hành 3', 2, 'Cao', False),
                ('Ôn tập Python cơ bản', 'Ôn list, dict, hàm và lớp', 5, 'Trung bình', False),
                ('Nộp báo cáo môn Cơ sở dữ liệu', 'Nộp qua link drive', -1, 'Cao', True),
                ('Mua sách lập trình web', '', 10, 'Thấp', False),
                ('Học Bootstrap 5', 'Xem lại grid, card, navbar', 7, 'Trung bình', True),
            ],
            'tranthib': [
                ('Chuẩn bị thuyết trình nhóm', 'Làm slide và luyện nói 10 phút', 3, 'Cao', False),
                ('Đọc tài liệu Django ORM', 'filter, exclude, order_by', 6, 'Trung bình', False),
                ('Dọn dẹp máy tính', '', 12, 'Thấp', False),
                ('Đăng ký lịch thi cuối kỳ', 'Đăng ký trên cổng thông tin', -2, 'Cao', True),
            ],
            'admin': [
                ('Kiểm tra hệ thống', 'Sao lưu dữ liệu định kỳ', 4, 'Trung bình', False),
            ],
        }
        users['admin'] = admin

        total = 0
        for username, items in data.items():
            user = users[username]
            user.tasks.all().delete()
            for title, desc, days, priority, done in items:
                Task.objects.create(
                    title=title, description=desc,
                    due_date=today + timedelta(days=days),
                    priority=priority, is_completed=done, owner=user,
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f'Đã tạo dữ liệu mẫu: {total} công việc.'))
        self.stdout.write('  admin      / admin123')
        self.stdout.write('  nguyenvana / Test@12345')
        self.stdout.write('  tranthib   / Test@12345')
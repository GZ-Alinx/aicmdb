from django.core.management.base import BaseCommand
from apps.aiauth.models import AIDepartment


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 创建部门初始化数据
        boarder = AIDepartment.objects.create(name="董事会", intro="董事会")
        developer = AIDepartment.objects.create(name="产品开发部", intro="产品设计，技术开发")
        operator = AIDepartment.objects.create(name="运营部", intro="客服运营，产品运营")
        saler = AIDepartment.objects.create(name="销售部", intro="销售产品")
        hr = AIDepartment.objects.create(name="人事部", intro="员工招聘，员工培训，员工考核")
        finance = AIDepartment.objects.create(name="财务部", intro="财务报表，财务审核")
        self.stdout.write('部门数据初始化成功')
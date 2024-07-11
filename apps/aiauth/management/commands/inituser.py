from django.core.management.base import BaseCommand
from apps.aiauth.models import AIUser, AIDepartment, UserStatusChoices



class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = AIDepartment.objects.get(name="董事会")
        developer = AIDepartment.objects.get(name="产品开发部")
        operator = AIDepartment.objects.get(name="运营部")
        saler = AIDepartment.objects.get(name="销售部")
        hr = AIDepartment.objects.get(name="人事部")
        finance = AIDepartment.objects.get(name="财务部")


        # 管理者董事会 都是超级管理员
        dongdong = AIUser.objects.create_superuser(email='itadminlx@163.com',
                                                   username='dongdong',
                                                   password='123456',
                                                   status=UserStatusChoices.ACTIVE,
                                                   department=boarder
                                                   )

        duoduo = AIUser.objects.create_superuser(email='1135189009@163.com',
                                                   username='duoduo',
                                                   password='123456',
                                                 status=UserStatusChoices.ACTIVE,
                                                 department=boarder
                                                 )
        zhangsan = AIUser.objects.create_user(email='zhangsan@163.com',
                                                   username='zhangsan',
                                                   password='123456',
                                                    status=UserStatusChoices.ACTIVE,
                                                    department=developer
                                              )
        lisi = AIUser.objects.create_user(email='lisi@163.com',
                                              username='lisi',
                                              password='123456',
                                          status=UserStatusChoices.ACTIVE,
                                              department=operator
                                              )
        wangwu = AIUser.objects.create_user(email='wangwu@163.com',
                                          username='wangwu',
                                          password='123456',
                                        status=UserStatusChoices.ACTIVE,
                                          department=hr
                                          )
        zhaoliu = AIUser.objects.create_user(email='zhaoliu@163.com',
                                            username='zhaoliu',
                                            password='123456',
                                             status=UserStatusChoices.ACTIVE,
                                            department=finance
                                            )
        sunqi = AIUser.objects.create_user(email='sunqi@163.com',
                                             username='sunqi',
                                             password='123456',
                                           status=UserStatusChoices.ACTIVE,
                                             department=saler
                                             )

        # 给部门指定leader和manager
        boarder.leader = dongdong
        boarder.manager = None

        developer.leader = zhangsan
        developer.manager =  dongdong

        operator.leader = lisi
        operator.manager = dongdong

        saler.leader = sunqi
        saler.manager = dongdong

        hr.leader =  wangwu
        hr.manager = duoduo

        finance.leader = zhaoliu
        finance.manager = duoduo

        # 数据保存
        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()
        self.stdout.write('初始用户创建成功')
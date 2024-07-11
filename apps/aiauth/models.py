from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,Group,Permission
from django.contrib.auth.hashers import make_password
from shortuuidfield import ShortUUIDField


class UserStatusChoices(models.IntegerChoices):
    # 激活的
    ACTIVE = 1
    # 未激活
    UNACTIVE = 2
    # 锁定
    LOCKED = 3


#  用户基础模型 object
class AIUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        创建用户
        """
        if not username:
            raise ValueError("必须设置用户信息")
        email = self.normalize_email(email)
        username = self.model(username=username, email=email, **extra_fields)
        username.password = make_password(password)
        username.save(using=self._db)
        return username

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
         创建用户
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserStatusChoices.UNACTIVE)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级用户必须设置 is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级用户必须设置 is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)




#  重写User
class AIUser(AbstractBaseUser, PermissionsMixin):
    """
    自定义User模型
    """

    # ShortUUIDField 这里使用随机UUID
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(
        # _("username"),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(blank=False)
    telephone = models.CharField(max_length=20, blank=True)
    is_staff = models.BooleanField(default=True)
    status = models.IntegerField(choices=UserStatusChoices, default=UserStatusChoices.ACTIVE)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey('AIDepartment', null=True, on_delete=models.SET_NULL, related_name='staffs', related_query_name='staffs')
    groups = models.ManyToManyField(
        Group,
        related_name='aiuser_set',  # 修改此处
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='aiuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='aiuser_set',  # 修改此处
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='aiuser',
    )


    #  数据库操作对象
    objects = AIUserManager()

    EMAIL_FIELD = "email"
    # 此处是用来鉴权的字段 USERNAME_FIELD
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS 指定哪些字段是必须要传的 但是不能重复USERNAME_FIELD设置中的包含
    REQUIRED_FIELDS = ["password"]

    class Meta:
        db_table = "ai_users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """

        return self.username

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username




class AIDepartment(models.Model):
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=200)
    # leader 一对一
    # related_name 通过aiuser对象访问
    # related_query_name 跨表查询时使用
    leader = models.OneToOneField(AIUser, null=True, on_delete=models.SET_NULL, related_name='leader_department', related_query_name='leader_department')
    # manager
    # 外键
    manager = models.ForeignKey(AIUser, null=True, on_delete=models.SET_NULL, related_name='manager_department', related_query_name='manager_department')
    class Meta:
        db_table = "ai_department"
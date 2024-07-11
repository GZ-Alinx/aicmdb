from rest_framework import serializers
from .models import AIUser, UserStatusChoices, AIDepartment
from rest_framework import exceptions



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,)
    password = serializers.CharField(max_length=20, min_length=6)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = AIUser.objects.filter(username=username).first()
            if not user:
                raise serializers.ValidationError('请输入正确的用户')
            if not user.check_password(password):
                raise serializers.ValidationError('请输入正确的密码')

            # 判断账号状态
            if user.status == UserStatusChoices.UNACTIVE:
                raise serializers.ValidationError('用户未激活')
            elif user.status == UserStatusChoices.LOCKED:
                raise serializers.ValidationError('用户已锁定，请联系管理员！')
            # 为了减少查询sql的次数 这里把user放到attrs中 方便在视图中使用
            attrs['user'] = user
        else:
            raise serializers.ValidationError('请传入账号和密码！')
        return attrs

class DepertmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIDepartment
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    # 序列化部门数据
    department = DepertmentSerializer()
    class Meta:
        model = AIUser  # 替换为你的用户模型
        # fields = "__all__"
        # 排除字段
        exclude = ['password','groups','user_permissions']


# 重置密码序列化
class ResetPwdSerializer(serializers.Serializer):
    oldpwd = serializers.CharField(min_length=6, max_length=20)
    pwd1 = serializers.CharField(min_length=6, max_length=20)
    pwd2 = serializers.CharField(min_length=6, max_length=20)

    def validate(self, attrs):
        oldpwd = attrs['oldpwd']
        pwd1 = attrs['pwd1']
        pwd2 = attrs['pwd2']

        user = self.context['request'].user
        if not user.check_password(oldpwd):
            raise exceptions.ValidationError("旧密码错误！")

        if pwd1 != pwd2:
            raise exceptions.ValidationError("两个新密码不一致！")
        return attrs
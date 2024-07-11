from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from django.conf import settings
import jwt
from jwt.exceptions import ExpiredSignatureError
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from django.contrib.auth.models import AnonymousUser



AIUser = get_user_model()


# 鉴权验证器 如果没有登录则不可继续进行后续操作 setting.py中进行设置
class LoginCheckMiddleware(MiddlewareMixin):
    keyword = "JWT"

    # 登录跳过鉴权白名单 可持续添加
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.white_list = ['/auth/login',]

    def process_view(self, request, view_func, view_args, view_kwargs):
        # 1 返回None 那么就会正常执行后续代码
        # 2 返回HttpResponse对象，讲不会执行视图，已经后续中间加代码

        # 将登录接口排除 不进行jwt鉴权
        if request.path in self.white_list:
            request.user = AnonymousUser()
            request.auth = None
            return None

        try:
            auth = get_authorization_header(request).split()
            print("authinfo:", auth)
            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError('请传入JWT')

            if len(auth) == 1:
                msg = '不可用的JWT请求头'
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = '不可用的JWT请求头！应该提供一个空格！'
                raise exceptions.AuthenticationFailed(msg)

            try:
                jwt_token = auth[1]
                jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms="HS256")
                print("解密后的jwt信息：", jwt_info)
                userid = jwt_info.get('userid')
                try:
                    print("查询数据开始")
                    user = AIUser.objects.get(pk=userid)
                    print("查询后的数据：", user)
                    setattr(request, 'user', user)
                    request.user = user
                    request.auth = jwt_token
                except Exception:
                    print("查询后的数据：", user)
                    msg = '用户不存在！'
                    raise exceptions.AuthenticationFailed(msg)
            except UnicodeError:
                msg = 'Token格式错误！'
                raise exceptions.AuthenticationFailed(msg)
            except ExpiredSignatureError:
                msg = 'JWT Token已过期！'
                raise exceptions.AuthenticationFailed(msg)
        except Exception as e:
            print("校验失败", e)
            return JsonResponse(data={"detail": "请先登录"}, status=HTTP_403_FORBIDDEN)
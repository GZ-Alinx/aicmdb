from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer, UserSerializer, ResetPwdSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        # 验证数据是否可用
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            token = generate_jwt(user)
            return Response({'token': token, 'user': UserSerializer(user).data})
        else:
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)


#  鉴权基类 拦截器 重复的写法
# class AuthenticatedRequiredView:
#     permission_classes = [IsAuthenticated]


class ResetPassword(APIView):
    # 继承拦截器 独立写法
    # class ResetPassword(APIView, AuthenticatedRequiredView):

    # 这里的request是drf封装的 rest_framework.request.Request
    # 鉴权写法
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request)
        print(request.user)
        serializer = ResetPwdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pwd1 = serializer.validated_data.get('pwd1')
            request.user.set_password(pwd1)
            request.user.save()
            return Response({'msg':'密码修改成功'})
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)
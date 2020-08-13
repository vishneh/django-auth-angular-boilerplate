from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

import random,math
from django.core.mail import send_mail
from django.shortcuts import render
from account.models import ForgotTokens, Account
from account.serializers import (
    UserRegisterSerializer,
    ResetPasswordSerializer,
    
)
# Create your views here.

@api_view(['POST',])
def UserRegistrationView(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save(user=request.user)
            data['message'] = "Sucessfully Registered"
            data['username'] = account.username
            token = Token.objects.get(user=account).key

            data['token'] = token
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ResetPasswordView(request):
    account = Account.objects.get(pk=request.user.user_id)
    if request.method == 'POST':
        serializer = ResetPasswordSerializer(account , data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            data = {"messaage" : "Password Updated Successfully",}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


@api_view(['POST', ])
def ForgotPasswordView(request):
    print(request.data.get('email'))
    try:
        account = Account.objects.get(email=request.data.get('email'))
    except :
        print("err")
        return Response(data, status=status.HTTP_403_FORBIDDEN)
        
    if request.method == 'POST':
        forgot_otp = "";
        for i in range(6):
            forgot_otp += str(math.floor(random.random() * 10))
        print(forgot_otp)
        forgotToken = ForgotTokens(
            user = account,
            forgot_otp = forgot_otp,
        )
        forgotToken.save()
        send_mail(
            'Forgot Password Code',
            forgotToken.forgot_otp,
            'archtamizh@gmail.com',
            ['vishnuprabhu.bvk@gmail.com'],
            fail_silently=False,
        )
        data = {"messaage" : "Password Updated Successfully",'otp': forgot_otp}
        return Response(data, status=status.HTTP_200_OK)
import random,math
from rest_framework import serializers
from django.core.mail import send_mail

from account.models import (
        Account, 
        UserModel, 
    )

class UserRegisterSerializer(serializers.ModelSerializer):
    
    password_confirm = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = Account
        fields = ['email','password','password_confirm','user_type',]
        extra_kwargs = {
            'password': {'write_only':True}
        }


    def save(self,user):
        email=self.validated_data['email'].lower(),
        username=self.validated_data['email'].lower(),
        account = Account(
            email=email[0],
            username=username[0],
            user_type = 1, ## Here is the Privilege Detail
        )
        password = self.validated_data['password']
        password_conifrm = self.validated_data['password_confirm']

        if password != password_conifrm:
            raise serializers.ValidationError({'password':'Password Doesnt match'})
        account.set_password(password)
        account.save()
        user_otp = "";
        for i in range(6):
            user_otp += str(math.floor(random.random() * 10))
        user = UserModel(
            user= account,
            user_otp= user_otp, 
        )
        user.save()
        send_mail(
            'Account Verification',
            user_otp,
            'archtamizh@gmail.com',
            ['vishnuprabhu.bvk@gmail.com'],
            fail_silently=False,
        )
        return account


class ResetPasswordSerializer(serializers.ModelSerializer):
    
    password_confirm = serializers.CharField()
    password_old = serializers.CharField()
    class Meta:
        model = Account
        fields = ['password_old','password_confirm','password']



    def save(self,account):
        password = self.validated_data['password']
        password_old = self.validated_data['password_old']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'message':'Password Doesnt match'})
        if not account.check_password(password_old):
            raise serializers.ValidationError({'message':'Old Password Doesnt Correct'})

        account.set_password(password)
        account.save()
        return account

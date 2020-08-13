from django.db import models

# For Account
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# For Auth Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime,timedelta


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    USER_TYPE_CHOICES = ((1,'user1'),(2, 'user2'),(3, 'user3'))
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30, unique=True)
    mobile_number 			= models.CharField(max_length=10, unique=True, blank=True, null=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser			= models.BooleanField(default=False)
    is_admin				= models.BooleanField(default=False)
    is_staff				= models.BooleanField(default=False)
    user_type               = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,null=True)


    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['mobile_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


# For Token If place this it will create Tokens By default
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class UserModel(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    # subscriber=models.BooleanField(default=False)
    user_is_active=models.BooleanField(default=False)

    first_name=models.CharField(max_length=30,blank=True, null=True)
    last_name=models.CharField(max_length=10,blank=True, null=True)
    user_address=models.CharField(max_length=200,blank=True, null=True)
    user_otp = models.PositiveSmallIntegerField()

    class Meta:
            verbose_name = "User"
    def __str__(self):
        return self.user.username


class ForgotTokens(models.Model):

    def now_plus_30():
        return datetime.now() + timedelta(minutes=30)

        
    user=models.OneToOneField(Account,on_delete=models.CASCADE)

    created_time = models.DateTimeField(default=datetime.now, blank=True)
    expiry_time = models.DateTimeField(default=now_plus_30 , blank=True)
    forgot_otp = models.PositiveSmallIntegerField()

    class Meta:
            verbose_name = "ForgotToken"
    def __str__(self):
        return self.user.username

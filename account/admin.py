from django.contrib import admin
from django.contrib.auth.models import Group
from account.models import (
    Account,
    UserModel,
    ForgotTokens,
)
# Register your models here.
admin.site.register(Account)
admin.site.register(UserModel)
admin.site.register(ForgotTokens)
# admin.site.register(Bearer)
admin.site.unregister(Group)
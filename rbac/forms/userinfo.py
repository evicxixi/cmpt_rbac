from django import forms
from rbac import models


class UserInfo(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'

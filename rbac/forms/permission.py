from django import forms
from rbac import models


class Permission(forms.ModelForm):

    class Meta:
        model = models.Permission
        fields = '__all__'

        widgets = {    # 单独定制前端渲染此field
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '权限名称为8-12个字符'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '含正则的URL'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL别名'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'menu': forms.Select(attrs={'class': 'form-control'}),

        }

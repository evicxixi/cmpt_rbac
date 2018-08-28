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


# 生成formset对象，关键词‘extra’决定生成form时默认填充的数据之外，再生成几个空form。
PermissionFormSet = forms.formset_factory(models.Permission, extra=10)

formset = PermissionFormSet(    # 实例化
    initial=[
        {
            'id': 1,
            'user': 'nut',
            'pwd': '123',
            'email': 'xxxx@live.com'
        },    # 生成form时默认填充的数据
        {
            'id': 2,
            'user': 'hat',
            'pwd': '1231',
            'email': 'xxxxd@live.com'
        }
    ]
)

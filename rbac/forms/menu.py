from django import forms
from rbac import models


class Menu(forms.ModelForm):

    class Meta:
        model = models.Menu
        fields = '__all__'

        widgets = {    # 单独定制前端渲染此field
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '菜单名称为8-12个字符'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入icon字符'}),
        }

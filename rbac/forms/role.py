from django import forms
from rbac import models


class Role(forms.ModelForm):

    class Meta:
        model = models.Role
        fields = '__all__'

        widgets = {    # 单独定制前端渲染此field
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

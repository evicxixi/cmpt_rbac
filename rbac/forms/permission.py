from django import forms
from rbac import models


class Permission(forms.ModelForm):

    class Meta:
        model = models.Permission
        fields = '__all__'

        widgets = {    # 单独定制前端渲染此field
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '权限名称为8-12个字符'}),
            'url': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '含正则的URL'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'URL别名'}),
            'parent': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'menu': forms.Select(attrs={'class': 'form-control form-control-sm'}),

        }


class MultiPermission(forms.Form):
    attrs = {'class': "form-control form-control-sm"}
    id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs=attrs),
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs=attrs),
    )
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs=attrs),
                           )
    parent = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs=attrs),
        required=False,
    )
    menu = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs=attrs),
        required=False,

    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].choices += models.Permission.objects.filter(parent_id__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')
        self.fields['menu'].choices += models.Menu.objects.values_list(
            'id', 'title')

    def clean_pid_id(self):
        menu = self.cleaned_data.get('menu_id')
        pid = self.cleaned_data.get('pid_id')
        if menu and pid:
            raise forms.ValidationError('菜单和根权限同时只能选择一个')
        return pid

    def clean(self):
        parent = self.cleaned_data['parent']
        self.cleaned_data['parent'] = models.Permission.objects.get(pk=parent)

        menu = self.cleaned_data['menu']
        self.cleaned_data['menu'] = models.Menu.objects.get(pk=menu)
        # print('clean', parent, menu)

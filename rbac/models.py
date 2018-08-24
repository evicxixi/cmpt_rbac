from django.db import models


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)

    # 将一级菜单升级为二级菜单 注释掉字段（is_menu，icon）增加（name,parent,menu）
    # parent 位于三级（并不真正属于三级） 关联二级菜单id 决定归属哪个二级菜单
    # menu 直接关联根菜单 决定是否属于二级菜单
    # 备注：parent与manu为非此即彼的关系

    # is_menu = models.BooleanField(
    #     verbose_name='是否是菜单', default=False)
    # icon = models.CharField(verbose_name='Icon',
    #                         max_length=32, null=True, blank=True)
    name = models.CharField(verbose_name='URL别名',
                            max_length=32, null=True, blank=True)
    parent = models.ForeignKey(
        verbose_name='父权限', to='Permission', null=True, blank=True)
    menu = models.ForeignKey(verbose_name='菜单', to='Menu',
                             null=True, blank=True, help_text='null表示非菜单')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(
        verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(
        verbose_name='拥有的所有角色', to='Role', blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    菜单
    将一级菜单升级为二级菜单增加此表
    """
    title = models.CharField(verbose_name='菜单', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title

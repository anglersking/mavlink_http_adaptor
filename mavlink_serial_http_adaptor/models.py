from django.db import models

# Create your models here.


class Users(models.Model):
    """定义用户的模型类"""

    # 定义系统
    GENSER_CHOICES = (
        (0, "linux"),
        (1, "win")
    )
    # 用户名最长10 admin显示名字  姓名
    uname = models.CharField(max_length=10, verbose_name="用户名")
    # null=True 可以为空 默认为False
    uage = models.IntegerField(null=True, verbose_name="年龄")
    umobile = models.CharField(max_length=11, null=True, verbose_name="手机号")
    # choices 指定性别  default默认值
    uos = models.IntegerField(choices=GENSER_CHOICES, default=0, verbose_name="系统")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_bbsuser"  # 数据库的表名
        verbose_name = "用户"  # 站点管理的名称
        verbose_name_plural = verbose_name  # 站点管理的复数

    def __str__(self):
        """数据对象显示的信息"""
        return self.uname


class BBSPost(models.Model):
    """论坛帖子的模型类"""
    btitle = models.CharField(max_length=200, verbose_name="帖子名字")
    bdate = models.DateField(verbose_name="发帖时间")
    bclick = models.IntegerField(default=0, verbose_name='点击次数')
    bcomment = models.IntegerField(default=0, verbose_name='回复次数')
    burl = models.CharField(default=0, max_length=100, verbose_name="链接")
    # 关联外键 User所关联的模型类类名， on_delete删除外键的效果,(()
    b_user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_bbsposts"
        verbose_name = '帖子'
        verbose_name_plural = verbose_name  # 区分中英文的复数

    def __str__(self):
        """对象显示的信息"""
        return self.btitle



# """
# 定义在view的同目录下
# """
from rest_framework import serializers  # 导包

from mavlink_serial_http_adaptor.models import Users, BBSPost


class UsersModelsSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = Users  # 指定用户的模型类
        fields = '__all__'  # 写法一：指定查询的字段　ａｌｌ代表全部
        # fields = ('id', 'uname', 'uage')  # 写法二：指定那些字段适用那谢字段做校验
        # read_only_fields = ('id',)  # 指明只读字段（用于序列化输出的字段）
        # exclude = ('is_delete',)  # 写法三：　排除掉那些字段



class BBSPostModelsSerializer(serializers.ModelSerializer):
    """帖子的序列化器"""
    class Meta:
        model = BBSPost
        fields = '__all__'
        extra_kwargs = {
            'bcomment': {'min_value': 0, 'required': True},
        }


# def this_uname(value):
#     """
#     函数名字随便
#     :param value:
#     :return:
#     """
#     if value not in 'drf':
#         raise serializers.ValidationError("用户名必须包含drf")
from mavlink_serial_http_adaptor.models import BBSPost, Users


class UsersSerializer(serializers.Serializer):
    """用户模型类序列化器
#     >>> from mavlink_serial_http_adaptor.serializers import UsersSerializer
# >>> from mavlink_serial_http_adaptor.models import Users
# >>> u=User.objects.get(id=1)
# >>> u=Users.objects.get(id=1)
# >>> us=UsersSerializer(u)
# >>> u.data

#  from mavlink_serial_http_adaptor.models import Users, BBSPost
# >>> from mavlink_serial_http_adaptor.serializers import UsersSerializer
# >>> u = Users.objects.all()
# >>> s = UsersSerializer(u, many=True)
# >>> s.data



    """
    GENSER_CHOICES = (
        (0, "man"),
        (1, "woman")
    )
    # read_only=True 表明该字段仅用于序列化输出
    id = serializers.IntegerField(label='ID', read_only=True)
    uname = serializers.CharField(label='用户名', max_length=10)  # validators=[this_uname])
    # required=False  可以不传
    uage = serializers.IntegerField(label='年龄', required=False)
    umobile = serializers.CharField(label='电话', required=False)
    # 外键一关联多的定义方法  结果'bbspost_set': [5, 11],
    bbspost_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    ugender = serializers.ChoiceField(choices=GENSER_CHOICES, label='性别', required=False)

    def validate_uname(self, value):
        """
        对名字添加单独的校验
        :param value: 要校验的数据
        :return: 对就饭会数据，错误返回错误信息
        """
        # 如果用户名不包含drf就抛出异常　反之正常将数据抛出
        if value not in 'drf':
            raise serializers.ValidationError("用户名必须包含drf")
        return value

    def create(self, validated_data):
        """添加数据"""
        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        更新数据
        :param instance: 要操作的对象
        :param validated_data:校验后的数据
        :return: 对象
        """
        instance.uname = validated_data.get('uname', instance.uname)
        instance.uage = validated_data.get('uage', instance.uage)
        instance.umobile = validated_data.get('umobile', instance.umobile)
        instance.ugender = validated_data.get('ugender', instance.ugender)
        instance.save()
        return instance


# 多对一
class BBSPostSerializer(serializers.Serializer):
    """帖子模型类序列化器"""
    id = serializers.IntegerField(label="ID", read_only=True)
    btitle = serializers.CharField(label="帖名", max_length=200, )
    bdate = serializers.DateField(label="发帖时间", required=False)
    bclick = serializers.IntegerField(label='点击次数', required=False)
    bcomment = serializers.IntegerField(required=False, label='回复次数')
    burl = serializers.CharField(max_length=100, label="链接", required=False)

    # 用法１ 结果　　'b_user': 6
    b_user = serializers.PrimaryKeyRelatedField(label='用户', read_only=True)
    # {'bdate': '2013-12-30', 'bclick': 33, 'burl': 'http://bbs.tianya.cn/post-414-71827-1.shtml',
    #  'btitle': '吉利汽车怎么样_delete': False, 'id': 3, 'b_user': 6, 'bcomment': 30}


    # 用法２ 结果　'b_user': '花满楼'（验证需要退出shell在进入）
    # 此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
    # b_user = serializers.StringRelatedField(label='用户', read_only=True)
    """
    b = BBSPost.objects.get(id=3)
    >> > b
    < BBSPost: 吉利汽车怎么样 >
    >> > bs = BBSPostSerializer(b)
    >> > bs.data
    {'is_delete': False, 'bclick': 33, 'id': 3, 'bcomment': 30, 'b_user': '花满楼', 'bdate': '2013-12-30', 'btitle': '吉利样',
     'burl': 'http://bbs.tianya.cn/post-414-71827-1.shtml'}
    """

    # 方法３　使用关联的类对象的序列化器　
    # 结果 'b_user': OrderedDict([('id', 2), ('uname', '墙角二枝梅'), ('uage', 37), ('umobile', '1666666888('ugender', 1), ('is_delete', False)])
    # b_user = UsersSerializer()
    """
        >>> b = BBSPost.objects.get(id=8)
    >>> bs = BBSPostSerializer(b)
    >>> bs.data
    {'bclick': 40, 'bcomment': 15, 'b_user': OrderedDict([('id', 4), ('uname', '煮酒论你妹'), ('uage', 20), ('umobile', '567345'), ('ugender', 0)]), 'bdate': '1999-06-04', 'btitle': '处女座', 'is_delete': False, 'id': 8, 'burl': 'http://btianya.cn/post-414-71827-1.shtml'}

    """

    # 方法４ slug_field="uage"  中的uage为关联对象的字段名   结果：'b_user': 37
    # b_user = serializers.SlugRelatedField(label="用户", read_only=True, slug_field="uage")
    """
        >>> b = BBSPost.objects.get(id=8)
    >>> b
    <BBSPost: 处女座>
    >>> bs = BBSPostSerializer(b)
    >>> bs.data
    {'btitle': '处女座', 'is_delete': False, 'id': 8, 'burl': 'http://bbs.tianya.cn/post-414-71827-1.shtml', 'bclick': 40bdate': '1999-06-04', 'b_user': 20, 'bcomment': 15}

    """
    # 方法 5 必须指明view_name参数，以便DRF根据视图名称寻找路由，进而拼接成完整URL
    # 结果　'b_user': 'http://127.0.0.1:8000/users/2/'
    # 没有视图无法演示
    # b_user = serializers.HyperlinkedRelatedField(view_name="ｘｘｘｘ"label="用户", read_only=True)

    is_delete = serializers.BooleanField(required=False, label="逻辑删除")

    def validate(self, attrs):
        """
        联合校验：同时对多个参数校验
        :param attrs: 经过初步校验后的数据
        :return:
        """
        if attrs["bclick"] < attrs['bcomment']:
            raise serializers.ValidationError("点击次数必须大于回复次数")
        return attrs

    def create(self, validated_data):
        """添加数据"""
        return BBSPost.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        更新数据
        :param instance: 对象
        :param validated_data: 校验后的数据
        :return: instance对象
        """
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bdate = validated_data.get("bdate", instance.bdate)
        instance.bclick = validated_data.get('bclick', instance.bclick)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.burl = validated_data.get('burl', instance.burl)
        instance.b_user_id = validated_data.get('b_user', instance.b_user)
        instance.save()
        return instance





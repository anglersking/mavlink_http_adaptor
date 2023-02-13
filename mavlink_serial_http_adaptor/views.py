from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json

# Create your views here.
from django.views import View
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet

from .models import Users
from .serializers import UsersModelsSerializer



class UsersViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersModelsSerializer

    @action(methods=['get'], detail=False)  # detail=False多个结果
    def latest(self, request):
        """
        返回最新的用户信息
        get users/latest/
        """
        users = Users.objects.latest('id')  # latest 倒序取第一个
        serializer = self.get_serializer(users)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)  # detail=True单一结果
    def update_uage(self, request, pk):
        """
        修改用户的年龄数据
        put users/3/update_uage/
        """
        users = self.get_object()
        users.uage = request.data.get('age')  # age必须和前端传入的一致
        users.save()
        serializer = self.get_serializer(users)
        return Response(serializer.data)


# users/2/
# class UsersViewSet(ReadOnlyModelViewSet):
#     queryset = Users.objects.all()
#     serializer_class = UsersModelsSerializer


class CheckAllUsers(ListAPIView):
    """实现所有发帖人员的的信息的查询"""

    serializer_class = UsersModelsSerializer
    queryset = Users.objects.all()


class CheckOneUsers(RetrieveAPIView):
    """查询单一的信息，只查一条结果"""
    serializer_class = UsersModelsSerializer
    queryset = Users.objects.all()


# users/1/
# class CheckOneUsers(RetrieveModelMixin, GenericAPIView):
#     """查询单一的信息，只查一条结果"""
#     serializer_class = UsersModelsSerializer
#     queryset = Users.objects.all()
#
#     def get(self, request, pk):
#         return self.retrieve(request)


# users/1/
# class CheckOneUsers(GenericAPIView):
#     """查询单一的信息，只查一条结果"""
#     queryset = Users.objects.all()
#     serializer_class = UsersModelsSerializer
#
#     def get(self, request, pk):
#         """查询单一的信息，只查一条结果"""
#
#         # lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
#         # lookup_field = 'pk'
#         # 得到真实的数据 单一的数据
#         data = self.get_object()
#         # 创建序列器对象
#         serializer = self.get_serializer(data)
#         # 响应
#         return Response(serializer.data)


# class CheckAllUsers(ListModelMixin, GenericAPIView):
#     """实现所有发帖人员的的信息的查询"""
#
#     serializer_class = UsersModelsSerializer
#     queryset = Users.objects.all()
#
#     def get(self, request):
#         return self.list(request)


# class CheckAllUsers(GenericAPIView):
#     """实现所有发帖人员的的信息的查询"""
#
#     queryset = Users.objects.all()
#     serializer_class = UsersModelsSerializer
#
#     def get(self, request):
#         """实现所有发帖人员的的信息的查询"""
#
#         # 得到真实的数据
#         data = self.get_queryset()
#         # 创建序列器对象
#         serializer = self.get_serializer(data, many=True)
#         # 响应
#         return Response(serializer.data)



# class CheckAllUsers(APIView):
#     """实现所有发帖人员的的信息的查询"""
#     # 可以校验　流量控制
#
#     def get(self, request):
#         """实现所有发帖人员的的信息的查询"""
#         # 1 准备数据
#         datas = Users.objects.all()
#         # ２　把数据交给序列化器
#         us = UsersModelsSerializer(datas, many=True)
#         # ３　处理
#         # ４　响应
#         return Response(us.data)


# users
# class CheckAllUsers(View):
#     """实现所有发帖人员的的信息的查询"""
#
#     def get(self, response):
#         datas = Users.objects.all()  # 查询所有的用户 　
#         users_lists = []
#         # ［{}, {},...］
#         for data in datas:
#             users_lists.append({
#                 'uname': data.uname,
#                 'uage': data.uage,
#                 'umobile': data.umobile,
#                 'ugender': data.ugender,
#                 'is_delete': data.is_delete
#             })
#         # 如果转列表，一定要写safe=false
#         return JsonResponse(users_lists, safe=False)



class ClassView(View):
    """类视图"""
    def get(self, request):
        """此函数执行的是get请求"""
        print("get请求")
        return HttpResponse("get")


    def post(self, request):
        """此函数执行的是post请求"""
        print('post请求')
        return HttpResponse('post')


def index(request):
    """
    视图函数
    :param request:  请求对像
    :return: ＯＫ
    测完
    """
    return HttpResponse('first_response')


def par_get(request, language, version):
    """获取用户请求ｕｒｌ的参数 测完"""
    # """http://127.0.0.1:8000/par_get/test/20"""

    print(language)
    print(version)

    return HttpResponse('par_get')


# /qd/?q=python&d=2019&d=2020
def qd(request):
    """获取ｕｒｌ查询字符串"""
    dicts = request.GET
    print(dicts.get('q'))
    # print(dicts['d'])
    print(dicts.getlist('d'))


    return HttpResponse('获取ｕｒｌ查询字符串')

def get_from_datas(request):
    """获取表单书据"""

    # 得到ｐｏｓｔ请求的数据
    dicts = request.POST
    print(dicts)

    # 对数据进行解析
    v = dicts.get('k')
    print(v)

    return HttpResponse('form_get')

def get_json(request):

    """获取非表单书据ｊｓｏｎ body raw
    测完
    """
    # 获取ｊｓｏｎ的书据
    datas_byt = request.body

    # 得到数据为ｂｙ需要转换
    datas = datas_byt.decode()
    # print(datas)
    # print(type(datas))

    # 得到的是字符串还得转换为ｄｉｃｔ
    dict_datas = json.loads(datas)


    print(dict_datas.get('a'))
    print(dict_datas.get('c'))
    # {"a": 1, "C": 2}

    return HttpResponse('获取非表单书据ｊｓｏｎ')


def set_cookies(request):
    """设置ｃｏｏｋｉｅｓ
    测完"""

    response = HttpResponse('OK')

    # name:cookie的名字　　python:cookie的值　　max_age过期时间
    response.set_cookie('name', 'python', max_age=3600)

    return response



def get_cookies(request):
    """读取ｃｏｏｋｉｅ
    测完"""

    # 得到对象的cookies属性
    dict_datas = request.COOKIES

    # 获取属性的ｖｅｌｕｅ
    print(dict_datas.get('name'))

    return HttpResponse('得到ｃｏｏｋｉｅｓ')



def set_get_sessions(request):
    """设置session,读取session
    测完
    """

    # 设置ｓｅｓｓｉｏｎ
    request.session['session123'] = 'python321321'

    # 获取ｓｅｓｓｉｏｎ
    request.session.get('session123')
    print(request.session.get('session123'))

    return HttpResponse('ok')


# def response_datas(reuqest):
#     """响应的内容"""
#     return HttpResponse(content='12345', content='jpg', starts=2000)


def redirect_response(request):
    """重定向"""
    # 原生重定向测完
    return redirect('/index/')

def response_json(request):
    """响应ｊｓｏｎ测完"""
    return JsonResponse({'name': '张三丰'})

















from django.conf.urls import url

from . import views
from rest_framework import routers

urlpatterns = [

    #index函数的路由
    url(r"^index/$", views.index),
    # test函数的url
    url(r'^par_get/(?P<language>[a-z]+)/(?P<version>\d+)/$', views.par_get),

    # qd函数的url
    url(r"^qd/$", views.qd),

    # get_from_datas函数的url
    url(r"^get_from_datas/$", views.get_from_datas),

    # get_json函数的ur
    url(r'^get_json/$', views.get_json),
    url(r"^classview/$", views.ClassView.as_view()),

    # # set_cookies的url
    # url(r"^set_cookies/$", views.set_cookies),
    #
    # set_cookies 的ｕｒｌ
    url(r"^set_cookies/$", views.set_cookies),

    # get_cookies 的ｕｒｌ
    url(r"^get_cookies/$", views.get_cookies),

    url(r"^set_get_sessions/$", views.set_get_sessions),

    # redirect_response函数的url
    url(r'^redirect_response/$', views.redirect_response),

    # response_json函数的url
    url(r"^response_json/$", views.response_json),

    url(r"^classview/$", views.ClassView.as_view()),
    #
    # # CheckAllUsers
    url(r"^users/$", views.CheckAllUsers.as_view()),
    #
    # # CheckOneUsers
    url(r"^users/(?P<pk>\d+)/$", views.CheckOneUsers.as_view()),

    # UsersViewSet
    url(r"^drfcheckusers/$", views.UsersViewSet.as_view({'get': 'list'})),
    #
    # # UsersViewSet
    url(r"^drfcheckusers/(?P<pk>\d+)/$", views.UsersViewSet.as_view({'get': 'retrieve'})),

    # UsersViewSet
    url(r"^users/latest$", views.UsersViewSet.as_view({'get': 'latest'})),

    # UsersViewSet
    url(r"^users/(?P<pk>\d+)/update_uage/$", views.UsersViewSet.as_view({'put': 'update_uage'})),




]

router = routers.SimpleRouter()
router.register(r'users', views.UsersViewSet, basename='user')
urlpatterns += router.urls
from django.conf.urls import url

from . import views

urlpatterns = [
# 注册人脸
    url('^registerface/$', views.RegisterFace.as_view()),

    # 人脸搜索
    url('^search/$', views.SearchFace.as_view()),

]
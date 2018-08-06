"""myblog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

import xadmin
from myblog.views import Login, Regsiter, Active, Logout, BlogDetail, BlogList, ResetUserInformation, Learn
from myblog.views import ResetLink, CommentManage, LearnList

urlpatterns = [
    path('sumcetadmin/', xadmin.site.urls, ),
    path('', BlogList.as_view(), name='index'),
    path('learn/', Learn.as_view(), name='learn'),
    path('learn/<int:blog_id>/', LearnList.as_view(), name='learnDetail'),
    path('aboutme/', TemplateView.as_view(template_name='aboutme.html'), name='aboutme'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Regsiter.as_view(), name='register'),
    path('resetlink/', ResetLink.as_view(), name='resetlink'),
    path('resetuser/<str:reset_code>/', ResetUserInformation.as_view(), name='resetuser'),
    path('active/<str:active_code>/', Active.as_view(), name='active'),
    path('blog/<int:blog_id>/', BlogDetail.as_view(), name='blogDetail'),
    path('comment/', CommentManage.as_view(), name='comment'),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

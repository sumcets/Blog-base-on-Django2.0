# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 16:10
# @Author  : 张坤
# @File    : adminx.py
# @Software: PyCharm
# @Contact : sumcets@gmail.com
import xadmin
from xadmin import views
from .models import BlogType, Blog, Comment, Tag, LearnShare



class BaseSetting():
    """
    设置主题
    """
    enable_themes = True
    use_bootswatch = True



class GlobalSettings():
    """
    设置页头页脚
    """
    site_title = 'sumcet博客后台管理系统'
    site_footer = 'sumcet'

class TagAdmin():
    list_display = ['name','color']
    search_field = ['name','color']
    list_filter = ['name','color']



class BlogTypeAdmin():
    list_display = ['typeName']
    search_field = ['typeName']
    list_filter = ['typeName']



class BlogAdmin():
    list_display = ['name', 'author', 'blog_type', 'create_time', 'last_updata_time', 'useful', 'id', 'tag']
    search_field = ['abstract','name', 'author', 'blog_type', 'create_time', 'last_updata_time', 'useful', 'id', 'tag']
    list_filter = ['abstract','name', 'author', 'blog_type', 'create_time', 'last_updata_time', 'useful', 'id', 'tag']



class LearnShareAdmin():
    list_display = ['name', 'author', 'share_type', 'create_time', 'last_updata_time', 'useful', 'id', 'tag']
    search_field = ['abstract', 'name', 'author', 'share_type', 'create_time', 'last_updata_time', 'useful', 'id', 'tag']
    list_filter = ['abstract', 'name', 'author', 'share_type', 'create_time', 'last_updata_time', 'useful', 'id', 'tag']





class CommentAdmin():
    list_display = ['comment_user', 'comment_time', 'comment_blog', 'comment_content']
    search_field = ['comment_user', 'comment_time', 'comment_blog', 'comment_content']
    list_filter = ['comment_user', 'comment_time', 'comment_blog', 'comment_content']


xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(BlogType, BlogTypeAdmin)
xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(LearnShare, LearnShareAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

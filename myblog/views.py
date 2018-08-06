import random
import string

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views.generic.base import View


from verfilycode.email_send import send_email, randomName
from .forms import LoginForms, RegisterForms, ResetLinkForms, ResetUserInformationForms
from .models import Blog, Comment, Tag, LearnShare


# 实现用户名和邮箱登陆
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登陆
class Login(View):
    original_page = ''
    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        loginform = LoginForms(request.POST)
        if loginform.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(Login.original_page, reverse('index'))
            else:
                return render(request, 'login.html', {'error_message': '密码或用户名错误'})
        else:
            return render(request, 'login.html', locals())

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'jump.html', {'msg': '您已经登陆，即将跳转到主页'})
        loginform = LoginForms()
        Login.original_page = request.GET.get('from','')
        return render(request, 'login.html', locals())



# 登出
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')



# 注册
class Regsiter(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'jump.html', {'msg': '您已经注册并登陆，即将跳转到主页'})
        register_form = RegisterForms()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        register_form = RegisterForms(request.POST)
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'msg': '邮箱已经存在'})
        if register_form.is_valid():
            user = User()
            user.username = randomName(email)
            user.password = make_password(password)
            user.is_active = False
            user.save()
            # 发送验证码，并将验证码和邮箱存入session
            code = ''.join(random.sample(string.ascii_letters + string.ascii_uppercase + string.digits, 20))
            email_title = 'sumcet博客激活链接'
            email_body = '点击链接激活账号：http://127.0.0.1:8000/active/{0}'.format(code)
            send_email(email, request, email_title, email_body, code)

            return render(request, 'jump.html', {'msg': '激活链接已经发送成功，激活后登陆'})
        else:
            return render(request, 'register.html', locals())



# 激活账户
class Active(View):
    def get(self, request, active_code):
        code = request.session.get('code', '')
        email = request.session.get('email', '')
        username = randomName(email)
        if active_code == code:
            User.objects.filter(username=username).update(is_active=True, email=email)
            # 激活后链接失效
            request.session["code"] = code + 'q'
            return render(request, 'jump_login.html', {'msg': '激活成功，正在跳转到登陆页面'})
        else:
            return HttpResponse('链接失效，请重新注册')



class ResetLink(View):
    def get(self, request):
        reset_link = ResetLinkForms()
        return render(request, 'resetlink.html', {'reset_link': reset_link})

    def post(self, request):
        reset_link = ResetLinkForms(request.POST)
        email = request.POST.get('email', '')
        if reset_link.is_valid():
            # 发送验证码，并将验证码和邮箱存入session
            code = ''.join(random.sample(string.ascii_letters + string.ascii_uppercase + string.digits, 20))
            email_title = 'sumcet博客重置用户信息链接'
            email_body = '点击链接重置信息：http://127.0.0.1:8000/resetuser/{0}'.format(code)
            send_email(email, request, email_title, email_body, code)
            return render(request, 'jump.html', {'msg': '重置链接已经发送成功'})



# 重置用户信息
class ResetUserInformation(View):
    def get(self, request, reset_code):
        code = request.session.get('code', '')
        email = request.session.get('email', '')
        resetUserInformation_forms = ResetUserInformationForms()
        if reset_code == code:
            return render(request, 'resetuserinformation.html',
                          {'email': email, 'resetUserInformation_forms': resetUserInformation_forms,
                           'reset_code': reset_code})
        return render(request, 'jump.html', {'msg': '出错了！请再试一次！'})

    def post(self, request, reset_code):
        code = request.session.get('code', '')
        email = request.session.get('email', '')
        pwd = request.POST.get('password', '')
        password = make_password(pwd)
        username = request.POST.get('username', '')
        if reset_code == code:
            User.objects.filter(email=email).update(is_active=True, password=password, username=username)
            # 重置后后链接失效
            request.session["code"] = code + 'q'
            return render(request, 'jump_login.html', {'msg': '重置成功，正在跳转到登陆页面'})
        else:
            return HttpResponse('链接失效，请在一个浏览器中进行操作')



class BlogDetail(View):
    def get(self, request, blog_id):
        # 获取标签
        tags = Tag.objects.all()
        # 热门评论
        hot = Comment.objects.all()
        if hot.count() <= 5:
            hot_comments = hot
        else:
            hot_comments = hot[:5]
        # 热门推荐
        hot_blog = Blog.objects.filter(hot='1')
        if hot_blog.count() <= 5:
            hot_blogs = hot_blog
        else:
            hot_blogs = hot_blog[:5]

        blogs = get_object_or_404(Blog, id=int(blog_id))
        comments = Comment.objects.filter(comment_blog__id=int(blog_id))

        blog_path = '/blog/'+str(blog_id)+'/'

        return render(request, 'detail.html', {'blog_path':blog_path,'tags':tags, 'blogs': blogs, 'comments': comments, 'hot_comments': hot_comments, 'hot_blogs':hot_blogs})



class BlogList(View):
    def get(self, request):
        # 获取全部blog
        blogs = Blog.objects.all()
        # 获取标签
        tags = Tag.objects.all()
        # 热门评论
        hot = Comment.objects.all()
        if hot.count() <= 5:
            hot_comments = hot
        else:
            hot_comments = hot[:5]
        # 热门推荐
        hot_blog = Blog.objects.filter(hot='1')
        if hot_blog.count() <= 5:
            hot_blogs = hot_blog
        else:
            hot_blogs = hot_blog[:5]
        try:
            paginator = Paginator(blogs, 5, allow_empty_first_page=True)
            page = request.GET.get('page', 1)
            contacts = paginator.get_page(int(page))
            return render(request, 'index.html', {'tags':tags, 'contacts': contacts, 'hot_comments': hot_comments,'hot_blogs':hot_blogs})
        except Exception as e:
            contacts = blogs
            return render(request, 'index.html', {'tags':tags, 'contacts': contacts, 'hot_comments': hot_comments,'hot_blogs':hot_blogs})



class Learn(View):
    def get(self, request):
        # 获取全部learn
        learns = LearnShare.objects.all()
        # 获取标签
        tags = Tag.objects.all()
        # 热门评论
        hot = Comment.objects.all()
        if hot.count() <= 5:
            hot_comments = hot
        else:
            hot_comments = hot[:5]
        # 热门推荐
        hot_blog = Blog.objects.filter(hot='1')
        if hot_blog.count() <= 5:
            hot_blogs = hot_blog
        else:
            hot_blogs = hot_blog[:5]
        try:
            paginator = Paginator(learns, 5, allow_empty_first_page=True)
            page = request.GET.get('page', 1)
            contacts = paginator.get_page(int(page))
            return render(request, 'learn.html', {'tags':tags, 'contacts': contacts, 'hot_comments': hot_comments,'hot_blogs':hot_blogs})
        except Exception as e:
            contacts = learns
            return render(request, 'learn.html', {'tags':tags, 'contacts': contacts, 'hot_comments': hot_comments,'hot_blogs':hot_blogs})



class LearnList(View):
    def get(self, request, blog_id):
        # 获取标签
        tags = Tag.objects.all()
        # 热门评论
        hot = Comment.objects.all()
        if hot.count() <= 5:
            hot_comments = hot
        else:
            hot_comments = hot[:5]
        # 热门推荐
        hot_blog = Blog.objects.filter(hot='1')
        if hot_blog.count() <= 5:
            hot_blogs = hot_blog
        else:
            hot_blogs = hot_blog[:5]

        blogs = get_object_or_404(LearnShare, id=int(blog_id))
        comments = Comment.objects.filter(comment_blog__id=int(blog_id))

        blog_path = '/learn/'+str(blog_id)+'/'

        return render(request, 'learndetail.html', {'blog_path':blog_path,'tags':tags, 'blogs': blogs, 'comments': comments, 'hot_comments': hot_comments, 'hot_blogs':hot_blogs})




class CommentManage(View):
    def post(self, request):
        # 返回原页面
        jump_page = request.META.get('HTTP_REFERER')

        comment_user = request.POST.get('username', '')
        comment_blog = request.POST.get('blog_id', '')
        comment_content = request.POST.get('comment_content', '')
        user = User.objects.get(username=comment_user)
        blog = Blog.objects.get(id=int(comment_blog))

        comment = Comment()
        comment.comment_user = user
        comment.comment_blog = blog
        comment.comment_content = comment_content
        comment.save()

        return redirect(jump_page)

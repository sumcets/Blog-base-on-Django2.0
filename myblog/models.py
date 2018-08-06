from django.contrib.auth.models import User
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.



class Tag(models.Model):
    choice = (
        ('label label-danger', '红色'),
        ('label label-default', '灰色'),
        ('label label-primary', '深蓝色'),
        ('label label-success', '绿色'),
        ('label label-info', '浅蓝色'),
        ('label label-warning', '橘黄色')
    )
    name = models.CharField(null=False, blank=False, max_length=20, verbose_name='标签')
    color = models.CharField(choices=choice,max_length=20, null=True, verbose_name='标签颜色')


    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class BlogType(models.Model):
    typeName = models.CharField(max_length=20, blank=False, null=False, verbose_name='博客类型')


    class Meta:
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.typeName



class Blog(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='文章标题')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    blog_type = models.ForeignKey(BlogType, verbose_name='博客类型', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_updata_time = models.DateTimeField(auto_now=True, verbose_name='最后更改时间')
    useful = models.CharField(max_length=1, choices=(('1', '有效'), ('2', '无效'),), default='1', verbose_name='文章是否有效')
    blog_contend = RichTextUploadingField(verbose_name='文章内容')
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, verbose_name='标签')
    hot = models.CharField(max_length=1, choices=(('1', '上热门'), ('2', '不上热门'),), default='2', verbose_name='文章是否推荐')
    abstract = models.TextField(verbose_name='内容摘要', null=True)


    class Meta:
        verbose_name = '博客内容'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.name



class LearnShare(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='文章标题')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    share_type = models.ForeignKey(BlogType, verbose_name='分享类型', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_updata_time = models.DateTimeField(auto_now=True, verbose_name='最后更改时间')
    useful = models.CharField(max_length=1, choices=(('1', '有效'), ('2', '无效'),), default='1', verbose_name='文章是否有效')
    share_content = RichTextUploadingField(verbose_name='文章内容')
    abstract = models.TextField(verbose_name='内容摘要', null=True)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, verbose_name='标签')


    class Meta:
        verbose_name = '分享内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Comment(models.Model):
    comment_user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING, verbose_name='评论人')
    comment_blog = models.ForeignKey(Blog, on_delete=models.DO_NOTHING, verbose_name='评论对象')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    comment_content = models.TextField(verbose_name='评论内容')


    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-comment_time']

    def __str__(self):
        return '{0}：{1}'.format(self.comment_user, self.comment_content)

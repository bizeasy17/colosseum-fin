import logging
from abc import ABCMeta, abstractmethod, abstractproperty

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from colosseum.utils import cache, cache_decorator, get_current_site
from mdeditor.fields import MDTextField
from notifications.models import Notification, notification_handler
from uuslug import slugify

logger = logging.getLogger(__name__)

LINK_SHOW_TYPE = (
    ('i', _('首页')),
    ('l', _('列表页')),
    ('p', _('报告页面')),
    ('a', _('全站')),
    ('s', _('友情链接页面')),
)


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    def save(self, *args, **kwargs):
        is_update_views = isinstance(self, CNFReport) and 'update_fields' in kwargs and kwargs['update_fields'] == [
            'views']
        if is_update_views:
            CNFReport.objects.filter(pk=self.pk).update(views=self.views)
        else:
            if 'slug' in self.__dict__:
                slug = getattr(self, 'title') if 'title' in self.__dict__ else getattr(
                    self, 'name')
                setattr(self, 'slug', slugify(slug))
            super().save(*args, **kwargs)

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass


class CNFReport(BaseModel):
    """报告"""
    STATUS_CHOICES = (
        ('d', _('草稿')),
        ('p', _('发表')),
    )
    COMMENT_STATUS = (
        ('o', _('打开')),
        ('c', _('关闭')),
    )

    title = models.CharField(_('标题'), max_length=200, unique=True)
    slug = models.SlugField(default='no-slug', max_length=200, blank=True)
    digest = models.CharField(_('摘要'), max_length=200, null=True, blank=True)
    body = MDTextField(_('正文'))
    pub_time = models.DateTimeField(
        _('发布时间'), blank=False, null=False, default=now)
    status = models.CharField(_('报告状态'), max_length=1,
                              choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField(
        _('评论状态'), max_length=1, choices=COMMENT_STATUS, default='o')
    views = models.PositiveIntegerField(_('浏览量'), default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('作者'), blank=False, null=False,
                               on_delete=models.CASCADE)
    report_order = models.IntegerField(
        _('排序,数字越大越靠前'), blank=False, null=False, default=0)
    category = models.ForeignKey(
        'Category', verbose_name=_('分类'), on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('Tag', verbose_name=_('标签集合'), blank=True)
    featured_image = models.ImageField(
        _('特色图片'), upload_to='report_pictures/%Y/%m/%d/')
    report_sourcefile = models.FileField(
        _('报告源数据文件'), upload_to='report_files/%Y/%m/%d/')
    report_sourcedata = models.TextField(_('报告源数据'), blank=False, null=False)
    to_placeholder = models.ForeignKey('PlaceHolder', verbose_name=_('栏目位'), blank=True, null=True,
                                       on_delete=models.SET_NULL)

    def body_to_string(self):
        return self.body

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-report_order', '-pub_time']
        verbose_name = _('数据和图表报告')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def get_absolute_url(self):
        return reverse('chartsnfigures:detailbyid', kwargs={
            'report_id': self.id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        tree = self.category.get_category_tree()
        names = list(map(lambda c: (c.name, c.get_absolute_url()), tree))

        return names

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def comment_list(self):
        cache_key = 'report_comments_{id}'.format(id=self.id)
        value = cache.get(cache_key)
        if value:
            logger.info('get report comments:{id}'.format(id=self.id))
            return value
        else:
            comments = self.comment_set.filter(is_enable=True)
            cache.set(cache_key, comments, 60 * 100)
            logger.info('set report comments:{id}'.format(id=self.id))
            return comments

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

    @cache_decorator(expiration=60 * 100)
    def next_report(self):
        # 下一篇
        return CNFReport.objects.filter(id__gt=self.id, status='p').order_by('id').first()

    @cache_decorator(expiration=60 * 100)
    def prev_report(self):
        # 前一篇
        return CNFReport.objects.filter(id__lt=self.id, status='p').first()


class Category(BaseModel):
    """报告分类"""
    name = models.CharField(_('分类名'), max_length=30, unique=True)
    parent_category = models.ForeignKey(
        'self', verbose_name=_('父级分类'), blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('分类')
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('chartsnfigures:category_detail', kwargs={'category_name': self.slug})

    def __str__(self):
        return self.name

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        """
        递归获得分类目录的父级
        :return: 
        """
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categorys

    @cache_decorator(60 * 60 * 10)
    def get_sub_categorys(self):
        """
        获得当前分类目录所有子集
        :return: 
        """
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)

        parse(self)
        return categorys


class Tag(BaseModel):
    """报告标签"""
    name = models.CharField(_('标签名'), max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chartsnfigures:tag_detail', kwargs={'tag_name': self.slug})

    @cache_decorator(60 * 60 * 10)
    def get_report_count(self):
        return CNFReport.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = _('标签')
        verbose_name_plural = verbose_name


class Links(models.Model):
    """友情链接"""

    name = models.CharField(_('链接名称'), max_length=30, unique=True)
    link = models.URLField(_('链接地址'))
    sequence = models.IntegerField(_('排序'), unique=True)
    is_enable = models.BooleanField(
        _('是否显示'), default=True, blank=False, null=False)
    show_type = models.CharField(
        _('显示类型'), max_length=1, choices=LINK_SHOW_TYPE, default='i')
    created_time = models.DateTimeField(_('创建时间'), default=now)
    last_mod_time = models.DateTimeField(_('修改时间'), default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = _('友情链接')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SideBar(models.Model):
    """侧边栏,可以展示一些html内容"""
    name = models.CharField(_('标题'), max_length=100)
    content = models.TextField(_('内容'))
    sequence = models.IntegerField(_('排序'), unique=True)
    is_enable = models.BooleanField(_('是否启用'), default=True)
    created_time = models.DateTimeField(_('创建时间'), default=now)
    last_mod_time = models.DateTimeField(_('修改时间'), default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = _('侧边栏')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


PLACEHOLDER_TYPE = (
    ('t', _('首页置顶')),
    ('l', _('首页列表页')),
    ('s', _('首页边栏')),
    ('r', _('人工推荐栏')),
)


class Placeholder(models.Model):
    """首页栏位,可以展示Report内容"""
    name = models.CharField(_('栏目名称'), max_length=100)
    # content = models.TextField(_('摘要内容'))
    # picked_report = models.ForeignKey(
    #     'CNFReport', on_delete=models.SET_NULL, verbose_name=_('标签集合'), null=True, blank=True)
    pl_type = models.CharField(
        _('栏位类型'), max_length=1, choices=PLACEHOLDER_TYPE, default='t')
    sequence = models.IntegerField(_('排序'), unique=True)
    is_enable = models.BooleanField(_('是否启用'), default=True)
    created_time = models.DateTimeField(_('创建时间'), default=now)
    last_mod_time = models.DateTimeField(_('修改时间'), default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = _('内容栏位')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class WebsiteSettings(models.Model):
    '''站点设置 '''
    sitename = models.CharField(
        _('网站名称'), max_length=200, null=False, blank=False, default='')
    site_description = models.TextField(
        _('网站描述'), max_length=1000, null=False, blank=False, default='')
    site_seo_description = models.TextField(
        _('网站SEO描述'), max_length=1000, null=False, blank=False, default='')
    site_keywords = models.TextField(
        _('网站关键字'), max_length=1000, null=False, blank=False, default='')
    cnfreport_sub_length = models.IntegerField(_('报告摘要长度'), default=300)
    sidebar_cnfreport_count = models.IntegerField(_('侧边栏报告数目'), default=10)
    sidebar_comment_count = models.IntegerField(_('侧边栏评论数目'), default=5)
    show_google_adsense = models.BooleanField(_('是否显示谷歌广告'), default=False)
    google_adsense_codes = models.TextField(
        _('广告内容'), max_length=2000, null=True, blank=True, default='')
    open_site_comment = models.BooleanField(_('是否打开网站评论功能'), default=True)
    beiancode = models.CharField(
        _('备案号'), max_length=2000, null=True, blank=True, default='')
    analyticscode = models.TextField(
        _('网站统计代码'), max_length=1000, null=False, blank=False, default='')
    show_gongan_code = models.BooleanField(
        _('是否显示公安备案号'), default=False, null=False)
    gongan_beiancode = models.TextField(
        _('公安备案号'), max_length=2000, null=True, blank=True, default='')
    resource_path = models.CharField(
        _('静态文件保存地址'), max_length=300, null=False, default='/var/www/resource/')

    class Meta:
        verbose_name = _('网站配置')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sitename

    def clean(self):
        if WebsiteSettings.objects.exclude(id=self.id).count():
            raise ValidationError(_('只能有一个配置'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from colosseum.utils import cache
        cache.clear()


def notify_comment(**kwargs):
    """Handler to be fired up upon comments signal to notify the author of a
    given report."""
    actor = kwargs['request'].user
    receiver = kwargs['comment'].content_object.user
    obj = kwargs['comment'].content_object
    notification_handler(
        actor, receiver, Notification.COMMENTED, action_object=obj
    )

import logging
from abc import ABCMeta, abstractmethod, abstractproperty

import tushare as ts
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from colosseum.utils import cache, cache_decorator, get_current_site
from uuslug import slugify

logger = logging.getLogger(__name__)

# Create your models here.
# token settings (to be moved)
ts.set_token('3ebfccf82c537f1e8010e97707393003c1d98b86907dfd09f9d17589')


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(_('创建时间'), default=now)
    last_mod_time = models.DateTimeField(_('修改时间'), default=now)

    # def save(self, *args, **kwargs):
    #     is_update_views = isinstance(self, TradeRec) and 'update_fields' in kwargs and kwargs['update_fields'] == [
    #         'views']
    #     if is_update_views:
    #         TradeRec.objects.filter(pk=self.pk).update(views=self.views)
    #     else:
    #         if 'slug' in self.__dict__:
    #             slug = getattr(self, 'stock_code') if 'stock_code' in self.__dict__ else getattr(
    #                 self, 'stock_name')
    #             setattr(self, 'slug', slugify(slug + id))
    #         super().save(*args, **kwargs)

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


MARKET_CHOICE = (
    ('sh', _('上海')),
    ('sz', _('深圳')),
)


class TradeRec(BaseModel):
    """交易记录"""
    STATUS_CHOICES = (
        ('d', _('草稿')),
        ('p', _('发表')),
    )
    # MARKET_CHOICES = (
    #     ('sa', _('上海A股')),
    #     ('p', _('发表')),
    # )
    VISIBLE_CHOICES = (
        ('g', _('公开')),
        ('s', _('私密')),
        ('f', _('仅好友')),
    )
    COMMENT_STATUS = (
        ('o', _('打开')),
        ('c', _('关闭')),
    )
    TRADE_DIRECTION = (
        ('b', _('买入')),
        ('s', _('卖出')),
    )
    TRADE_FLAG = (
        ('s', _('首次建仓')),
        ('n', _('正常买入/卖出')),
        ('l', _('清仓')),
    )

    # slug = models.SlugField(default='no-slug', max_length=200, blank=True)
    market = models.CharField(
        _('股票市场'), choices=MARKET_CHOICE, max_length=50, blank=True, null=True)
    stock_name = models.CharField(
        _('股票名称'), max_length=50, blank=False, null=False)
    stock_code = models.CharField(
        _('股票代码'), max_length=50, blank=False, null=False)
    direction = models.CharField(_('交易类型'), max_length=1,
                                 choices=TRADE_DIRECTION, default='b')
    flag = models.CharField(_('交易标签'), max_length=1,
                            choices=TRADE_FLAG, default='b', blank=True, null=True)
    # 交易日期
    trade_time = models.DateTimeField(
        '交易时间', default=now, blank=False, null=False)
    price = models.FloatField(_('交易价格'), blank=False, null=False)
    cash = models.FloatField(_('投入现金额'), blank=True, null=True)
    lots = models.PositiveIntegerField(_('买入量（手）'), default=100)
    position = models.CharField(
        _('本次交易仓位'), max_length=50, blank=False, null=False)
    pub_time = models.DateTimeField(
        _('发布时间'), blank=False, null=False, default=now)
    status = models.CharField(_('发布状态'), max_length=1,
                              choices=STATUS_CHOICES, default='p')
    visible = models.CharField(_('可见性'), max_length=1,
                               choices=VISIBLE_CHOICES, default='s')
    comment_status = models.CharField(
        _('评论状态'), max_length=1, choices=COMMENT_STATUS, default='c')
    views = models.PositiveIntegerField(_('浏览量'), default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('创建者'), blank=False, null=False,
                               on_delete=models.CASCADE)
    strategy = models.ForeignKey(
        'TradeStrategy', verbose_name=_('策略'), on_delete=models.SET_NULL, blank=True, null=True)
    # tags = models.ManyToManyField('Tag', verbose_name=_('标签集合'), blank=True)
    featured_image = models.ImageField(
        _('特色图片'), upload_to='traderec_pictures/%Y/%m/%d/', blank=True, null=True)
    # total_hold_positions = models.ForeignKey('Positions', verbose_name=_('股票持仓'), blank=False, null=False,
    #                            on_delete=models.CASCADE)
    is_deleted = models.CharField(
        _('是否被删除'), max_length=1, blank=False, null=False, default='n', editable=False)

    def __str__(self):
        return self.stock_name

    class Meta:
        ordering = ['-pub_time']
        verbose_name = _('交易记录')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def get_absolute_url(self):
        return reverse('traderec:detailbyid', kwargs={
            'traderec_id': self.id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    # @cache_decorator(60 * 60 * 10)
    def get_strategy_tree(self):
        tree = self.strategy.get_strategy_tree()
        names = list(map(lambda s: (s.name, s.get_absolute_url()), tree))

        return names

    def save(self, *args, **kwargs):
        if self.stock_code.isnumeric():
            self.stock_code = self.stock_code + '.' + self.market
        # 更新持仓
        Positions.objects.pos_cal_algorithm(, self)
        super().save(*args, **kwargs)

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def comment_list(self):
        comments = self.comment_set.filter(is_enable=True)
        logger.info('set report comments:{id}'.format(id=self.id))
        return comments

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

    def next_rec(self):
        # 下一篇
        return TradeRec.objects.filter(id__gt=self.id, status='p').order_by('id').first()

    def prev_rec(self):
        # 前一篇
        return TradeRec.objects.filter(id__lt=self.id, status='p').first()

# 目前持有仓位数据model


class Positions(BaseModel):
    market = models.CharField(
        _('股票市场'), choices=MARKET_CHOICE, max_length=50, blank=True, null=True)
    stock_name = models.CharField(
        _('股票名称'), max_length=50, blank=False, null=False)
    stock_code = models.CharField(
        _('股票代码'), max_length=50, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('持仓人'), blank=False, null=False,
                               on_delete=models.CASCADE)
    position_price = models.FloatField(
        _('持仓价格'), blank=False, null=False, default=0)
    current_price = models.FloatField(
        _('股票现价'), blank=False, null=False, default=0)
    profit = models.FloatField(_('利润'), blank=False, null=False)
    cash = models.FloatField(_('投入现金额'), blank=True, null=True)
    lots = models.PositiveIntegerField(_('买入量（手）'), default=100)
    position = models.CharField(
        _('仓位'), max_length=50, blank=False, null=False)
    is_liquadated = models.CharField(
        _('是否清仓'), max_length=1, blank=False, null=False, default='n', editable=false, db_index=True)

    def __str__(self):
        return self.stock_name

    # 持仓算法
    def pos_cal_algorithm(TradeRec):
        user = get_user_model()
        trade_rec = TradeRec
        ts_code = trade_rec.stock_code
        trade_price = trade_rec.price
        df = ts.get_realtime_quotes(ts_code)
        realtime_price = df[['price']]
        current_stock_position = Positions.objects.get(author=user,stock_code=ts_code,is_liquadated='n')

        # 已经有持仓
        if current_stock_position is not None:
            if trade_rec.direction == 'b':
                # 已有仓位加仓
                '''
                1. 利润 = 原持仓利润 + (当前股票价格：如果未收盘/收盘价 - 交易价格) * 本次交易量(手) * 100 (1手=100股)
                2. 
                '''
                profit = current_stock_position.profit + (realtime_price - trade_price) * trade_rec.lots * 100
                
                new_position_price = realtime_price - profit / (trade_rec.lots + current_stock_position.lots)
            else: # 已有仓位减仓
                if trade_rec.flag == 'l':
                    # 清仓，设置is_liquadated = 'y'

                else:

        else:  # 新建仓
            profit = (realtime_price - trade_price) * trade_rec.lots * 100
            p = Positions(trade_rec.stock_code[:2], trade_rec.stock_name, trade_rec.stock_code, u,
                          trade_rec.price, profit, trade_rec.cash, trade_rec.lots, trade_rec.position)
            p.save()

    class Meta:
        ordering = ['-last_mod_time']
        verbose_name = _('持仓')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

# 目前股票名字代码表


class StockNameCodeMap(BaseModel):
    DELIST_CHOICE = (
        ('y', _('退市')),
        ('n', _('可交易')),
    )

    market = models.CharField(
        _('股票市场'), choices=MARKET_CHOICE, max_length=50, blank=True, null=True)
    stock_name = models.CharField(
        _('股票名称'), max_length=50, blank=False, null=False, unique=True)
    stock_code = models.CharField(
        _('股票代码'), max_length=50, blank=False, null=False, unique=True)
    is_valid = models.CharField(
        _('是否退市'), choices=DELIST_CHOICE, max_length=1, blank=False, null=False, default='n')

    def __str__(self):
        return self.stock_name

    class Meta:
        ordering = ['-last_mod_time']
        verbose_name = _('股票代码表')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'


class TradeStrategy(BaseModel):
    """"""
    name = models.CharField(_('策略名'), max_length=30, unique=True)
    parent_strategy = models.ForeignKey(
        'self', verbose_name=_('父级策略'), blank=True, null=True, on_delete=models.CASCADE)
    # slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('交易策略')
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('traderec:strategy_detail', kwargs={'strategy_name': self.slug})

    def __str__(self):
        return self.name

    def get_strategy_tree(self):
        """
        递归获得策略目录的父级
        :return: 
        """
        strategies = []

        def parse(strategy):
            strategies.append(strategy)
            if strategy.parent_strategy:
                parse(strategy.parent_strategy)

        parse(self)
        return strategies

    def get_sub_strategies(self):
        """
        获得当前分类目录所有子集
        :return: 
        """
        strategies = []
        all_strategies = TradeStrategy.objects.all()

        def parse(strategy):
            if strategy not in strategies:
                strategies.append(strategy)
            childs = all_strategies.filter(parent_strategy=strategy)
            for child in childs:
                if strategy not in strategies:
                    strategies.append(child)
                parse(child)

        parse(self)
        return strategies


class Tag(BaseModel):
    """交易记录标签"""
    name = models.CharField(_('标签名'), max_length=30, unique=True)
    # slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('traderec:tag_detail', kwargs={'tag_name': self.slug})

    # @cache_decorator(60 * 60 * 10)
    def get_traderec_count(self):
        return TradeRec.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = _('标签')
        verbose_name_plural = verbose_name

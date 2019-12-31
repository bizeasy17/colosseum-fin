from django.db import models
from django.conf import settings
from chartsnfigures.models import CNFReport
from django.utils.timezone import now
from django.utils.translation import ugettext as _


# Create your models here.

class Comment(models.Model):
    body = models.TextField(_('正文'), max_length=300)
    created_time = models.DateTimeField(_('创建时间'), default=now)
    last_mod_time = models.DateTimeField(_('修改时间'), default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('作者'), on_delete=models.CASCADE)
    cnfreport = models.ForeignKey(CNFReport, verbose_name=_('数据图表报告'), on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name=_('上级评论'), blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField(_('是否显示'), default=True, blank=False, null=False)

    class Meta:
        ordering = ['id']
        verbose_name = _('评论')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

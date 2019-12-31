from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class commands(models.Model):
    title = models.CharField(_('命令标题'), max_length=300)
    command = models.CharField(_('命令'), max_length=2000)
    describe = models.CharField(_('命令描述'), max_length=300)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    last_mod_time = models.DateTimeField(_('修改时间'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('命令')
        verbose_name_plural = verbose_name


class EmailSendLog(models.Model):
    emailto = models.CharField(_('收件人'), max_length=300)
    title = models.CharField(_('邮件标题'), max_length=2000)
    content = models.TextField(_('邮件内容'))
    send_result = models.BooleanField(_('结果'), default=False)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('邮件发送log')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

import logging

import django
import django.dispatch
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.signals import (user_logged_in, user_logged_out,
                                         user_login_failed)
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

import _thread
from chartsnfigures.models import (Category, CNFReport, Links, SideBar, Tag,
                                   WebsiteSettings)
from comments.models import Comment
from comments.utils import send_comment_email

from .spider_notify import SpiderNotify
from .utils import (cache, delete_sidebar_cache, delete_view_cache,
                    expire_view_cache, get_current_site, send_email)

logger = logging.getLogger(__name__)

oauth_user_login_signal = django.dispatch.Signal(providing_args=['id'])
send_email_signal = django.dispatch.Signal(providing_args=['emailto', 'title', 'content'])


@receiver(send_email_signal)
def send_email_signal_handler(sender, **kwargs):
    emailto = kwargs['emailto']
    title = kwargs['title']
    content = kwargs['content']

    msg = EmailMultiAlternatives(title, content, from_email=settings.DEFAULT_FROM_EMAIL, to=emailto)
    msg.content_subtype = "html"

    from servermgr.models import EmailSendLog
    log = EmailSendLog()
    log.title = title
    log.content = content
    log.emailto = ','.join(emailto)

    try:
        result = msg.send()
        log.send_result = result > 0
    except Exception as e:
        logger.error(e)
        log.send_result = False
    log.save()


@receiver(post_save)
def model_post_save_callback(sender, instance, created, raw, using, update_fields, **kwargs):
    clearcache = False
    if isinstance(instance, LogEntry):
        return
    if 'get_full_url' in dir(instance):
        is_update_views = update_fields == {'views'}
        if not settings.TESTING and not is_update_views:
            try:
                notify_url = instance.get_full_url()
                SpiderNotify.baidu_notify([notify_url])
            except Exception as ex:
                logger.error("notify sipder", ex)
        if not is_update_views:
            clearcache = True
    if isinstance(instance, Comment):

        path = instance.cnfreport.get_absolute_url()
        site = get_current_site().domain
        if site.find(':') > 0:
            site = site[0:site.find(':')]

        expire_view_cache(path, servername=site, serverport=80, key_prefix='blogdetail')
        if cache.get('seo_processor'):
            cache.delete('seo_processor')
        comment_cache_key = 'cnfreport_comments_{id}'.format(id=instance.cnfreport.id)
        cache.delete(comment_cache_key)
        delete_sidebar_cache(instance.author.username)
        delete_view_cache('cnfreport_comments', [str(instance.cnfreport.pk)])

        _thread.start_new(send_comment_email, (instance,))

    if clearcache:
        cache.clear()


@receiver(user_logged_in)
@receiver(user_logged_out)
def user_auth_callback(sender, request, user, **kwargs):
    if user and user.username:
        logger.info(user)
        delete_sidebar_cache(user.username)
        cache.clear()

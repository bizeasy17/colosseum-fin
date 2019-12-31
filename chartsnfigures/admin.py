from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

# Register your models here.
# , Links, SideBar, BlogSettings
from .models import Category, CNFReport, Links, SideBar, Tag, WebsiteSettings

# @admin.register(CNFReport)
class CNFReportListFilter(admin.SimpleListFilter):
    title = _('作者')
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = list(set(map(lambda x: x.author, CNFReport.objects.all())))
        for author in authors:
            yield (author.id, _(author.username))

    def queryset(self, request, queryset):
        id = self.value()
        if id:
            return queryset.filter(author__id__exact=id)
        else:
            return queryset


class CNFReportForm(forms.ModelForm):
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = CNFReport
        fields = '__all__'

# admin.site.register(CNFReport)

def makr_article_publish(modeladmin, request, queryset):
    queryset.update(status='p')


def draft_article(modeladmin, request, queryset):
    queryset.update(status='d')


def close_article_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='c')


def open_article_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='o')


makr_article_publish.short_description = _('发布选中文章')
draft_article.short_description = _('选中文章设置为草稿')
close_article_commentstatus.short_description = _('关闭文章评论')
open_article_commentstatus.short_description = _('打开文章评论')


class CNFReportAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'title')
    form = CNFReportForm
    list_display = (
        'id', 'title', 'author', 'link_to_category', 'created_time', 'views', 'status', 'report_order')
    list_display_links = ('id', 'title')
    list_filter = (CNFReportListFilter, 'status', 'category', 'tags')
    filter_horizontal = ('tags',)
    exclude = ('created_time', 'last_mod_time')
    view_on_site = True
    actions = [makr_article_publish, draft_article,
               close_article_commentstatus, open_article_commentstatus]

    def link_to_category(self, obj):
        info = (obj.category._meta.app_label, obj.category._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.category.id,))
        return format_html(u'<a href="%s">%s</a>' % (link, obj.category.name))

    link_to_category.short_description = _('分类目录')

    def get_form(self, request, obj=None, **kwargs):
        form = super(CNFReportAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].queryset = get_user_model(
        ).objects.filter(is_superuser=True)
        return form

    def save_model(self, request, obj, form, change):
        super(CNFReportAdmin, self).save_model(request, obj, form, change)

    def get_view_on_site_url(self, obj=None):
        if obj:
            url = obj.get_full_url()
            return url
        else:
            from colosseum.utils import get_current_site
            site = get_current_site().domain
            return site

admin.site.register(CNFReport, CNFReportAdmin)


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'created_time')

# admin.site.register(Tag, TagAdmin)

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'created_time')

# admin.site.register(Category, CategoryAdmin)

class LinksAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'created_time')

# admin.site.register(Links, LinksAdmin)

class SideBarAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'is_enable', 'sequence')
    exclude = ('last_mod_time', 'created_time')

# admin.site.register(SideBar, SideBarAdmin)

class WebsiteSettingsAdmin(admin.ModelAdmin):
    pass

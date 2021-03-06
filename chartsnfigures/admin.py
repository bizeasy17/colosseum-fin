from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .forms import CNFReportForm
from .models import (Category, CNFReport, Links, Placeholder, SideBar, Tag,
                     WebsiteSettings)


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



# admin.site.register(CNFReport)

def makr_report_publish(modeladmin, request, queryset):
    queryset.update(status='p')


def draft_report(modeladmin, request, queryset):
    queryset.update(status='d')


def close_report_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='c')


def open_report_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='o')


makr_report_publish.short_description = _('发布选中报告')
draft_report.short_description = _('选中报告设置为草稿')
close_report_commentstatus.short_description = _('关闭报告评论功能')
open_report_commentstatus.short_description = _('打开报告评论功能')


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
    actions = [makr_report_publish, draft_report,
               close_report_commentstatus, open_report_commentstatus]

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


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'created_time')



class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'created_time')



class LinksAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'created_time')


class SideBarAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'is_enable', 'sequence')
    exclude = ('last_mod_time', 'created_time')

class CNFReportInline(admin.TabularInline):
    model = CNFReport
    fieldsets = (
        (_('基本信息'), {
            "fields": (
                'title', 'digest', 'views', 'category', 'pub_time'
            ),
        }),
        (_('详细内容'), {
            'classes': ('collapse',),
            'fields': ( 'author', 'tags', ),
        }),
    )
    
    extra = 5

class PlaceholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'pl_type', 'is_enable', 'sequence')
    exclude = ('slug', 'last_mod_time', 'created_time')
    # inlines = [CNFReportInline]


class WebsiteSettingsAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(CNFReport, CNFReportAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(SideBar, SideBarAdmin)
admin.site.register(Placeholder, PlaceholderAdmin)

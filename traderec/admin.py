from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .forms import TradeRecForm
from .models import TradeRec, TradeStrategy, Positions, StockNameCodeMap

# Register your models here.


class TradeRecListFilter(admin.SimpleListFilter):
    title = _('作者')
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = list(set(map(lambda x: x.author, TradeRec.objects.all())))
        for author in authors:
            yield (author.id, _(author.username))

    def queryset(self, request, queryset):
        id = self.value()
        if id:
            return queryset.filter(author__id__exact=id)
        else:
            return queryset


# class TradeRecAdmin(admin.ModelAdmin):
#     list_per_page = 20
#     search_fields = ('stock_name', 'stock_code')
#     form = TradeRecForm
#     list_display = (
#         'id', 'author', 'stock_name', 'direction', 'price', 'link_to_strategy', 'created_time', 'views')
#     list_display_links = ('id', 'stock_name')
#     list_filter = (TradeRecListFilter, 'status', 'strategy', 'flag')
#     # filter_horizontal = ('flag',)
#     exclude = ('created_time', 'last_mod_time')
#     view_on_site = True
#     # actions = [makr_report_publish, draft_report,
#     #            close_report_commentstatus, open_report_commentstatus]

#     def link_to_strategy(self, obj):
#         info = (obj.strategy._meta.app_label, obj.strategy._meta.model_name)
#         link = reverse('admin:%s_%s_change' % info, args=(obj.strategy.id,))
#         return format_html(u'<a href="%s">%s</a>' % (link, obj.strategy.name))

#     link_to_strategy.short_description = _('交易策略')

#     def get_form(self, request, obj=None, **kwargs):
#         form = super(TradeRecAdmin, self).get_form(request, obj, **kwargs)
#         form.base_fields['author'].queryset = get_user_model(
#         ).objects.filter(is_superuser=True)
#         return form

#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         super(TradeRecAdmin, self).save_model(request, obj, form, change)

#     def get_view_on_site_url(self, obj=None):
#         if obj:
#             url = obj.get_full_url()
#             return url
#         else:
#             from colosseum.utils import get_current_site
#             site = get_current_site().domain
#             return site

class TradeRecAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('stock_name', 'stock_code')
    list_display = (
        'author', 'stock_name', 'stock_code', 'direction', 'price', 'created_time')
    list_display_links = ('stock_name', 'stock_code')
    list_filter = (TradeRecListFilter, 'status', 'strategy', 'flag')
    exclude = ('created_time', 'last_mod_time')

class StrategyAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'created_time')


class TradePositionAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'created_time')


class StockNameCodeMapAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'created_time')


# Register your models here.
admin.site.register(TradeRec, TradeRecAdmin)
admin.site.register(TradeStrategy, StrategyAdmin)
admin.site.register(Positions, TradePositionAdmin)
admin.site.register(StockNameCodeMap, StockNameCodeMapAdmin)

from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.
class IndexView(ListView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'traderec/traderec_list.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'traderec_index'

    def get_queryset(self):
        traderec_list = TradeRec.objects.filter(status='p')
        return traderec_list

from datetime import datetime

import tushare as ts
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import FormView

from colosseum.helpers import AuthorRequiredMixin

# sample form
from .forms import NameForm, TradeRecForm
from .models import TradeRec, TradeStrategy

# token settings (to be moved)
ts.set_token('3ebfccf82c537f1e8010e97707393003c1d98b86907dfd09f9d17589')


def get_name(request, ts_code):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('Hello')

    # if a GET (or any other method) we'll create a blank form
    else:
        df = []
        # create a form instance and populate it with data from the request:
        df = ts.get_realtime_quotes(ts_code)
        return JsonResponse(df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']], safe=False)

    return render(request, 'traderec/name.html', {'form': form})

def get_stockcode(request, stock_name):
    if request.method == 'POST':
        return HttpResponse('000001.SZ')
    else:
        return HttpResponse('000001.SZ')
    return HttpResponse('000001.SZ')

def get_stockname(request, stock_code):
    if request.method == 'POST':
        return HttpResponse('平安银行')
    else:
        return HttpResponse('平安银行')
    return HttpResponse('平安银行')

def get_realtime_quotes(request, ts_code):
     # if this is a GET request we need to process the form data
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('Hello')
    else:
        df = []
        if request.method == 'GET':
            # create a form instance and populate it with data from the request:
            df = ts.get_realtime_quotes(ts_code)
            # return JsonResponse(df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']], safe=False)
            return HttpResponse(df['name'])

    return HttpResponse('hello')


def get_stock_kline(request, ts_code, start_date, end_date):
    df = []

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('Hello')
    else:
        # if this is a GET request we need to process the form data
        pro = ts.pro_api()

        if request.method == 'GET':
            # create a form instance and populate it with data from the request:
            df = pro.daily(ts_code=ts_code, start_date=start_date,
                        end_date=end_date)
            data = []
            if df is not None and len(df) > 0:
                for d in df.values:
                    data.append(
                        {
                            't': datetime.strptime(d[1], "%Y%m%d"),
                            'o': d[2],
                            'h': d[3],
                            'l': d[4],
                            'c': d[5],
                        }
                    )
            return JsonResponse(data[::-1], safe=False)
    return JsonResponse(df, safe=False)

# Create your views here.


class IndexView(ListView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'traderec/traderec_list.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'traderec_index'

    def get_queryset(self):
        traderec_list = TradeRec.objects.filter(status='p')
        return traderec_list


class TradeRecCreateView(LoginRequiredMixin, FormView):
    # model = TradeRec
    """Basic CreateView implementation to create new articles."""
    model = TradeRec
    message = _("Your article has been created.")
    form_class = TradeRecForm
    template_name = 'traderec/traderec_create.html'

    def form_valid(self, form):
        user = self.request.user
        # form.instance.user = user
        traderec = form.save(False)
        traderec.author = user
        traderec.save(True)
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('traderec:create_new')


class TradeRecUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = TradeRec
    form_class = TradeRecForm

    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'traderec/traderec_update.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'traderec_update'

    def get_queryset(self):
        traderec_list = TradeRec.objects.filter(status='p')
        return traderec_list


class TradeRecDetailView(LoginRequiredMixin, DetailView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'traderec/traderec_detail.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'traderec_detail'

    # def get_queryset(self):
    #     traderec_list = TradeRec.objects.filter(status='p')
    #     return traderec_list


class TradeRecHistoryView(LoginRequiredMixin, DetailView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'traderec/traderec_history.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'traderec_history'

    def get_queryset(self):
        traderec_list = TradeRec.objects.filter(status='p')
        return traderec_list

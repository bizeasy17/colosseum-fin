import random
from datetime import datetime

import tushare as ts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
from .models import TradeRec, TradeStrategy, Positions, StockNameCodeMap

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


@login_required
def get_stockcode_by_name(request, stock_name):
    if request.method == 'GET':
        result = StockNameCodeMap.objects.filter(stock_name=stock_name)
        if result is not None:
            for r in result:
                return HttpResponse(r.stock_code)
    return HttpResponse(_('无法找到该股票'))


@login_required
def get_stockname_by_code(request, stock_code):
    if request.method == 'GET':
        result = StockNameCodeMap.objects.filter(stock_code=stock_code)
        if result is not None:
            for r in result:
                return HttpResponse(r.stock_name)
    return HttpResponse(_('无法找到该股票'))


@login_required
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


@login_required
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
# @login_required


def get_stock_kline_ext(request, ts_code, start_date, end_date):
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
            traderec = []
            if df is not None and len(df) > 0:
                for d in df.values:
                    trade_datetime = datetime.strptime(d[1], "%Y%m%d")
                    traderec = get_traderec(ts_code, trade_datetime)
                    data.append(
                        {
                            't': trade_datetime,
                            'o': d[2],
                            'h': d[3],
                            'l': d[4],
                            'c': d[5],
                            'r': traderec,
                        }
                    )
            return JsonResponse(data[::-1], safe=False)
    return JsonResponse(df, safe=False)


def get_traderec(stock_code, trade_time):
    traderec_list = TradeRec.objects.filter(
        stock_code=stock_code, trade_time=trade_time)

    traderec = []
    if traderec_list is not None:
        for rec in traderec_list:
            traderec.append({
                'name': rec.stock_name,
                'code': rec.stock_code,
                'direction': rec.direction,
                'price': rec.price,
                'cash': rec.cash,
            })

    return traderec

def traderec_create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Post(text=post_text, author=request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username

        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})

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
    message = _('新的交易记录创建成功.')
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

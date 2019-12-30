# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'chartsnfigures/index.html'
    context_object_name = 'selected_chartsnfigures_list'

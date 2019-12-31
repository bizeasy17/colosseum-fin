# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from .models import CNFReport


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'chartsnfigures/index.html'
    context_object_name = 'selected_chartsnfigures_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return CNFReport.objects.order_by('-pub_time')[:5]

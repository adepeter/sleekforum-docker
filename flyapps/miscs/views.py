from django.shortcuts import render

from ..threads.models import Thread

from .forms.search import BaseSearchForm

# Create your views here.

def search(request):
    start_search = False
    form = BaseSearchForm(data=request.GET)
    results = None
    if form.is_valid():
        cleaned_name = form.cleaned_data['text']
        results = Thread.objects.filter(title__icontains=cleaned_name)
        start_search = True
    context = {
        'form': form,
        'start_search': start_search,
        'results': results,
    }
    return render(request, 'flyapps/miscs/search/index.html', context=context)
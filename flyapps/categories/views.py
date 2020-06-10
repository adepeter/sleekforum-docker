from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.urls import reverse

from ..threads.models.thread import Thread
from .models import Category
from .viewmixins.category import ListViewMixin


TEMPLATE_URL = 'flyapps/categories'


class ListBaseCategory(ListView):
    template_name = f'{TEMPLATE_URL}/category_list.html'
    model = Category
    context_object_name = 'categories'


class ListCategory(ListViewMixin):
    template_name = f'{TEMPLATE_URL}/subcategory_list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        parent_node_obj = self.get_parent_node_obj()
        return parent_node_obj.get_children()

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_parent_node_obj()
        if obj.threads.exists():
            kwargs = {
                'category_id': obj.id,
                'category_slug': obj.slug
            }
            return HttpResponseRedirect(reverse('flyapps:threads:list_threads', kwargs=kwargs))
        return super().dispatch(request, *args, **kwargs)


class ListDescendantCategoryThread(ListViewMixin):
    model = Thread
    template_name = f'{TEMPLATE_URL}/thread_list.html'
    context_object_name = 'threads'

    def get_queryset(self):
        parent_node_obj = self.get_parent_node_obj()
        qs = self.model.objects.filter(
            category__in=parent_node_obj.get_descendants(include_self=True),
            is_hidden=False,
        )
        return qs


class SearchCategory(ListView):
    model = Category
    template_name = f'{TEMPLATE_URL}/search_category.html'
    context_object_name = 'categories'

    def get(self, request, *args, **kwargs):
        self.keyword = self.request.GET.get('keyword')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET:
            return qs.filter(
                Q(name__iexact=self.request.GET.get('keyword')) |
                Q(description__icontains=self.request.GET.get('keyword')) |
                Q(slug__iexact=self.request.GET.get('keyword'))
            )
        return qs.none()

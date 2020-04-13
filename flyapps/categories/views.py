from django.views.generic import ListView

from ..threads.models.thread import Thread
from .models import Category
from .viewmixins.category import ListViewMixin

# Create your views here.

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

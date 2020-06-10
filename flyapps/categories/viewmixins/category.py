from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from ..models import Category


class CategoryQuerysetMixin:

    def get_queryset(self):
        raise NotImplementedError('Please override the get_queryset() \
        method of this view')

    def get_parent_node_obj(self):
        return get_object_or_404(
            Category,
            pk=self.kwargs.get('pk'),
            slug__iexact=self.kwargs.get('slug')
        )


class ListViewMixin(CategoryQuerysetMixin, ListView):
    """
    Base Inheritance to be used in view
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_node'] = self.get_parent_node_obj()
        return context

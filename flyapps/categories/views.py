from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Category

# Create your views here.

TEMPLATE_URL = 'flyapps/categories'


class CategoryList(ListView):
    template_name = f'{TEMPLATE_URL}/category_list.html'
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubcategoryList(ListView):
    template_name = f'{TEMPLATE_URL}/subcategory_list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        self.parent_category = get_object_or_404(Category, slug__iexact=self.kwargs['category_slug'])
        return self.parent_category.get_children()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.parent_category
        return context
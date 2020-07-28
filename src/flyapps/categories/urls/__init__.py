from django.urls import include, path
from ..views import (
    ListBaseCategory,
    ListCategory,
    ListDescendantCategoryThread,
    SearchCategory,
)

app_name = 'categories'

urlpatterns = [
    path('', ListBaseCategory.as_view(), name='list_category'),
    path('search/', SearchCategory.as_view(), name='search_category'),
]

urlpatterns += [
    path('<int:pk>/<slug:slug>/', include([
        path('', ListCategory.as_view(), name='list_subcategory'),
        path('threads/', ListDescendantCategoryThread.as_view(), name='list_thread'),
    ]))
]

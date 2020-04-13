from django.urls import include, path
from ..views import (
    ListBaseCategory,
    ListCategory,
    ListDescendantCategoryThread
)

app_name = 'categories'

urlpatterns = [
    path('', ListBaseCategory.as_view(), name='list_category'),
    path('<slug:slug>/', include([
        path('', ListCategory.as_view(), name='list_subcategory'),
        path('threads/', ListDescendantCategoryThread.as_view(), name='list_thread'),
    ]))
]
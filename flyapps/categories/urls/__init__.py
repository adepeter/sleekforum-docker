from django.urls import path
from .. import views

app_name = 'categories'

urlpatterns = [
    path('', views.CategoryList.as_view(), name='categories'),
    path('<slug:category_slug>/', views.SubcategoryList.as_view(), name='subcategories'),
]
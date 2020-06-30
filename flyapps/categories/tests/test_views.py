from django.test import TestCase
from django.urls import reverse
from mptt.querysets import TreeQuerySet

from flyapps.categories.models import Category

TEMPLATE_URL = 'flyapps/categories'


class BaseCategoryViewTest(TestCase):

    def setUp(self):
        self.base_category_1 = Category.objects.create(name='Programming')
        self.base_category_2 = Category.objects.create(name='News')
        self.base_category_3 = Category.objects.create(name='Technology', slug='tech')

    def test_root_view_exists(self):
        response = self.client.get(reverse('flyapps:categories:list_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['categories'])
        self.assertTrue(response.context['object_list'])
        self.assertIsInstance(response.context['categories'], TreeQuerySet)
        self.assertTemplateUsed(response, f'{TEMPLATE_URL}/category_list.html')

    def test_category_queryset(self):
        response = self.client.get(reverse('flyapps:categories:list_category'))
        self.assertContains(response, self.base_category_1)
        self.assertContains(response, self.base_category_2)
        self.assertContains(response, self.base_category_3)
        self.assertEqual(Category.objects.count(), 3)

    def test_category_redirects_to_children(self):
        base_category = Category.objects.get(name__iexact='programming')
        children_names = ['Python', 'Java', 'C++']
        for children in children_names:
            Category.objects.create(name=children, parent=base_category)
        self.assertEqual(base_category.slug, 'programming')
        # kwargs = {
        #     'pk': base_category.pk,
        #     'slug': base_category.slug
        # }
        # self.assertRedirects(
        #     base_category,
        #     reverse('flyapps:categories:list_subcategory', kwargs=kwargs)
        # )

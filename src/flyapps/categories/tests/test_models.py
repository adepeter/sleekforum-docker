from django.db import IntegrityError
from django.test import TestCase

from ..models import Category


class CategoryTestModel(TestCase):
    def setUp(self):
        self.base_category_1 = Category.objects.create(name='Programming')
        self.base_category_2 = Category.objects.create(name='News')
        self.base_category_3 = Category.objects.create(name='Technology', slug='tech')

    def test_category_valid_create(self):
        category_1 = self.base_category_1
        children_category_1 = category_1.children.create(name='Python')
        self.assertEqual(category_1.name, 'Programming')
        self.assertEqual(children_category_1.parent, category_1)
        self.assertEqual(Category.objects.count(), 4)

    def test_invalid_category_create(self):
        category_2 = self.base_category_2
        with self.assertRaises(IntegrityError):
            invalid_category_by_slug = Category.objects.create(
                parent=category_2,
                name='Technology',
                slug='tech'
            )

from django.test import TestCase


from ..models import Category

class TestModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Programming')

    def test_category_create(self):
        self.assertEqual(self.category.name, 'Programming')
        self.assertEqual(self.category.slug, 'programming')
class BaseSingleObjectMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])


class BaseLikeMixin:
    pass


class BaseDislikeMixin:
    pass


class BaseHideMixin:
    pass

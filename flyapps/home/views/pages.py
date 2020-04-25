from django.views.generic import FormView, TemplateView

TEMPLATE_URL = 'flyapps/home/pages'


class ContactUs(FormView):
    pass


class GlobalSearch(FormView):
    pass


class GlobalStatistics(TemplateView):
    template_name = f'{TEMPLATE_URL}/statistics.html'

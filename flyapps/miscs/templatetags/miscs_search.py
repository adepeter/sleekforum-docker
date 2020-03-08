from django import template

register = template.Library()

@register.inclusion_tag('flyapps/miscs/search.html')
def search(param):
    form = ''
    context = {
        'form': form
    }
    return context
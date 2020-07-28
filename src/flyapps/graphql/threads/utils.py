from django.utils.text import slugify


def slugify_tags(serialized_data):
    if 'tags' in serialized_data:
        return serialized_data.update(
            {'tags': [slugify(x) for x in serialized_data['tags']]}
        )

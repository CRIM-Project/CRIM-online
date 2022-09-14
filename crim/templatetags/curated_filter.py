from django.template.defaulttags import register

@register.filter(name='filter_curated')
def filter_curated(list):
    for item in list:
        if item['curated']:
            yield item

@register.filter(name='curated_count')
def curated_count(list):
    return sum(1 for item in list if item['curated'])

@register.filter(name='filter_uncurated')
def filter_uncurated(list):
    for item in list:
        if not item['curated']:
            yield item

@register.filter(name='uncurated_count')
def uncurated_count(list):
    return sum(1 for item in list if not item['curated'])

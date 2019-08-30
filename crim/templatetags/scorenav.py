from django.template.defaultfilters import register


@register.filter(name='prevpage')
def prevpage(request):
    '''Goes to the previous page using the ?p= parameter.'''
    current_page_number = eval(request.GET.get('p', '1'))
    previous_page_number = current_page_number - 1
    if previous_page_number < 1:
        previous_page_number = 1
    return '?p={}#score'.format(str(previous_page_number))

@register.filter(name='start')
def start(request):
    '''Goes to the first page.'''
    return '?#score'

@register.filter(name='nextpage')
def prevpage(request):
    '''Goes to the next page using the ?p= parameter.'''
    current_page_number = eval(request.GET.get('p', '1'))
    next_page_number = current_page_number + 1
    return '?p={}#score'.format(str(next_page_number))

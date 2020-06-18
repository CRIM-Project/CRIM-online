from django.template.defaultfilters import register


@register.filter(name='start')
def start(request):
    '''Goes to the default page.'''
    return '?'

@register.filter(name='prevpage')
def prevpage(request, current_page_number=1):
    '''Goes to the previous page using the `?p=` parameter.'''
    previous_page_number = current_page_number - 1
    if previous_page_number < 1:
        previous_page_number = 1
    return '?p={}'.format(str(previous_page_number))

@register.filter(name='nextpage')
def nextpage(request, current_page_number=1):
    '''Goes to the next page using the ?p= parameter.'''
    return '?p={}'.format(str(current_page_number + 1))


@register.filter(name='start_model')
def start_model(request):
    '''Goes to the default page of the model, while keeping the
    `?pd` parameter intact.'''
    # Collect derivative page number, if present
    current_derivative_page_number = eval(request.GET.get('pd', '0'))
    if current_derivative_page_number:
        derivative_parameter = 'pd={}'.format(current_derivative_page_number)
    else:
        derivative_parameter = ''
    return '?{}'.format(derivative_parameter)

@register.filter(name='prevpage_model')
def prevpage_model(request, current_model_page_number=1):
    '''Goes to the previous page of the model using the `?pm=`
    parameter, while keeping the `?pd` parameter intact.
    '''
    # Calculate new model page number
    previous_model_page_number = current_model_page_number - 1
    if previous_model_page_number < 1:
        previous_model_page_number = 1

    # Collect derivative page number, if present
    current_derivative_page_number = eval(request.GET.get('pd', '0'))
    if current_derivative_page_number:
        derivative_parameter = '&pd={}'.format(current_derivative_page_number)
    else:
        derivative_parameter = ''

    return '?pm={}{}'.format(str(previous_model_page_number), derivative_parameter)

@register.filter(name='nextpage_model')
def nextpage_model(request, current_model_page_number=1):
    '''Goes to the next page of the model using the `?pm=`
    parameter, while keeping the `?pd` parameter intact.
    '''
    # Calculate new model page number
    next_model_page_number = current_model_page_number + 1

    # Collect derivative page number, if present
    current_derivative_page_number = eval(request.GET.get('pd', '0'))
    if current_derivative_page_number:
        derivative_parameter = '&pd={}'.format(current_derivative_page_number)
    else:
        derivative_parameter = ''

    return '?pm={}{}'.format(str(next_model_page_number), derivative_parameter)


@register.filter(name='start_derivative')
def start_derivative(request):
    '''Goes to the default page of the derivative, while keeping the
    `?pm` parameter intact.'''
    # Collect model page number, if present
    current_model_page_number = eval(request.GET.get('pm', '0'))
    if current_model_page_number:
        model_parameter = 'pm={}'.format(current_model_page_number)
    else:
        model_parameter = ''
    return '?{}'.format(model_parameter)

@register.filter(name='prevpage_derivative')
def prevpage_derivative(request, current_derivative_page_number=1):
    '''Goes to the previous page of the derivative using the `?pd=`
    parameter, while keeping the `?pm` parameter intact.
    '''
    # Calculate new derivative page number
    previous_derivative_page_number = current_derivative_page_number - 1
    if previous_derivative_page_number < 1:
        previous_derivative_page_number = 1

    # Collect model page number, if present
    current_model_page_number = eval(request.GET.get('pm', '0'))
    if current_model_page_number:
        model_parameter = 'pm={}&'.format(current_model_page_number)
    else:
        model_parameter = ''

    return '?{}pd={}'.format(model_parameter, str(previous_derivative_page_number))

@register.filter(name='nextpage_derivative')
def nextpage_derivative(request, current_derivative_page_number=1):
    '''Goes to the next page of the derivative using the `?pd=`
    parameter, while keeping the `?pm` parameter intact.
    '''
    # Calculate new derivative page number
    next_derivative_page_number = current_derivative_page_number + 1

    # Collect model page number, if present
    current_model_page_number = eval(request.GET.get('pm', '0'))
    if current_model_page_number:
        model_parameter = 'pm={}&'.format(current_model_page_number)
    else:
        model_parameter = ''

    return '?{}pd={}'.format(model_parameter, str(next_derivative_page_number))

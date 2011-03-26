
def get_client_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])


from django import template

register = template.Library()

@register.filter
def get_request_status_list(value):
    return ['pending', 'approved', 'rejected', 'info_required']

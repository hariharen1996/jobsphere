from django import template 
from django.utils.timesince import timesince


register = template.Library()

@register.filter
def timesince_without_hrs(value):
    time_str = timesince(value)
    #print(f"time: {time_str}")
    time_sp = time_str.split()
    #print(time_sp)

    
    if 'hour' in time_str:
        time_sp = time_sp[:-2]
    
    #print(time_sp)
    return ' '.join(time_sp).strip(",")
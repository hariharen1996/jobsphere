from django import template 
from django.utils.timesince import timesince
from django.utils.safestring import mark_safe


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


@register.filter(name='get_reaction')
def get_reaction(reactions, reply_id):
    return reactions.get(reply_id)


@register.filter
def rating_smiley(value):
    print(value)
    if value == 1:
        return mark_safe("&#128577;")
    elif value == 2:
        return mark_safe("&#128528;")
    elif value == 3:
        return mark_safe("&#128578;")
    elif value == 4:
        return mark_safe("&#128522;")
    elif value == 5:
        return mark_safe("&#128512;")
    return mark_safe("&#129312")


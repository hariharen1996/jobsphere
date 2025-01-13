from django import template 
from django.utils.timesince import timesince
from django.utils.safestring import mark_safe


register = template.Library()

from django.utils.timesince import timesince
from datetime import datetime
import pytz

@register.filter
def timesince_without_hrs(value):
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    
    if value.tzinfo is None:
        value = pytz.utc.localize(value) 

    localtimezone = pytz.timezone('Asia/Kolkata') 
    local_time = value.astimezone(localtimezone)
    time = timesince(local_time)
    splitime = time.split()
    if 'hour' in time:
        splitime = splitime[:-2]

    return ' '.join(splitime).strip(",")


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


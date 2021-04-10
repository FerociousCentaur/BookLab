from django import template

register = template.Library()

@register.filter(name='get_list')
def get_list(value):
   #print(type(value))
   #print(type(eval(value)))# convert string to list
   return eval(value)
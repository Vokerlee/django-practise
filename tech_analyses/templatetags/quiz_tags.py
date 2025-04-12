from django import template

register = template.Library()

@register.filter
def lookup(value, arg):
    return value[arg]

@register.filter
def enum(sequence):
    try:
        result = list(enumerate(sequence))  # Uses built-in enumerate
        print(f"Enum input: {sequence}, output: {result}")  # Debug
        return result
    except Exception as e:
        print(f"Enumerate error: {e}")
        return []

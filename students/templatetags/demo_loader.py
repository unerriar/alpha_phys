from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True)
def load_demo_part(context, slug, part):
    """
    Loads a demo part (theory or controls) based on slug.
    Usage: {% load_demo_part demo.slug 'theory' %}
    """
    template_path = f'demos/{slug}/{part}.html'
    try:
        return render_to_string(template_path, context.flatten())
    except Exception:
        return f"<!-- Missing demo part: {template_path} -->"

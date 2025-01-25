from django.contrib import admin
from django.shortcuts import render


def c_render(request, html_file, context=None, show_error=False, error_message="", error_type="danger") -> dict:
    context.update(**admin.site.each_context(request))
    context['show_error'] = show_error
    context['error_message'] = error_message
    context['error_type'] = error_type
    return render(request, html_file, context=context)

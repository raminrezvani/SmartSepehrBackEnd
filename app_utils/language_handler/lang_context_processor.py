# from django.utils import translation


def lang_context_processor(request):

    # --- response
    return {
        "lang": "sv"
    }

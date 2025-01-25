from django.conf import settings


def change_ckeditor_images(ckeditor_content: str) -> str:
    """
    change ckeditor images path
    :param ckeditor_content: ckeditor content
    :return ckeditor content with absolute images
    """
    base_url = settings.SITE_URL
    old_value = "/media/ckeditor/"
    current_value = f"{base_url}{old_value}"
    return ckeditor_content.replace(old_value, current_value)

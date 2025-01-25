from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app_utils.lang_helper import get_current_language
from messages import messages


def get_message(lang: str, code: int) -> str:
    """
    get message with language
    :param lang: language code
    :param code: message code
    :return: message
    """
    current_lang = get_current_language()
    translation.activate(lang)
    default_message = _("not found")
    message = messages.get(code, default_message)
    translation.activate(current_lang)
    return message

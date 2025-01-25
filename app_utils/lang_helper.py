from django.conf import settings
from django.utils import translation
from rest_framework import status as rest_status


def get_current_language():
    """
    get current language
    :return: activate language code
    """
    return translation.get_language()


def is_valid_lang(lang) -> bool:
    """
    check if lang is valid in this project or not
    :param lang: language code that you want to validation
    :return: True => lang is valid
    """
    return lang in (valid_lang[0] for valid_lang in settings.LANGUAGES)


def validation_lang_response(lang) -> dict:
    """
    check if lang is valid in this project or not
    :param lang: language code that you want to validation
    :return: status, data, message, response_status
    """
    # --- not valid
    if not is_valid_lang(lang=lang):
        return {
            "status": False,
            "data": [],
            "message": [{'id': 1012, "field": "lang"}],
            "response_status": rest_status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    # --- valid
    return {
        "status": True,
        "data": [],
        "message": [{'id': 1011, "field": "ok"}],
        "response_status": rest_status.HTTP_200_OK
    }


def get_text_translation(lang: str, text: str) -> str:
    """
    get translation of text
    :param lang: language code
    :param text: text that you want to translate
    :return: translate of text if exists, if not response itself
    """
    with translation.override(lang):
        return translation.gettext(text)

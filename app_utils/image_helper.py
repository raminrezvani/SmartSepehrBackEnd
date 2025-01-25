import os

from PIL import Image
from django.conf import settings


def get_image_width_height(image_path: str) -> dict:
    """
    get image path and return width and height
    :param image_path: image path
    :return: dict with width and height value
    """
    im = Image.open(image_path)

    width, height = im.size
    return {'width': width, 'height': height}


def get_image_name(image_path: str) -> dict:
    """
    get image name and extension
    :param image_path: path for image
    :return: filename, extension
    """
    filename, file_extension = os.path.splitext(image_path)
    filename = os.path.basename(image_path)
    return {
        "filename": filename.replace(file_extension, ''),
        "extension": file_extension[1:]
    }


def crop_image(image_path: str, new_width: [int, float], new_height: [int, float], save_path: str) -> dict:
    """
    crop image with custom size (just center)
    :param image_path: path for image
    :param new_width: new image width
    :param new_height: new image height
    :param save_path: path for new image
    :return: status, content, path
    """
    try:
        im = Image.open(image_path)
        width, height = im.size  # Get dimensions

        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        im = im.crop((left, top, right, bottom))

        im.save(save_path)

        return {'status': True, "content": im, "path": save_path}
    except:
        return {'status': False, "content": "", "path": ""}


def resize_image(image_path: str, new_width: [int, float], new_height: [int, float], save_path: str) -> dict:
    """
    resize image with custom size
    :param image_path: path for image
    :param new_width: new image width
    :param new_height: new image height
    :param save_path: path for new image
    :return: status, content, path
    """
    im = Image.open(image_path)

    im.thumbnail((new_width, new_height))

    im.save(save_path)

    return {'status': True, }


def convert_image_to_webp(image_path: str, quality: int) -> str:
    """
    convert image to webp
    :param image_path: path for image that you want to change format
    :param quality: webp quality
    :return: new image path
    """
    media_path = settings.MEDIA_ROOT
    image_path = str(media_path / image_path)
    file_size = round(os.path.getsize(image_path) / 1024 ** 1, 3)  # kb
    if file_size > 85:
        file, ext = os.path.splitext(image_path)
        im = Image.open(image_path).convert("RGB")
        im.save(file + ".webp", "WEBP", optimize=True, quality=quality)
        os.remove(image_path)
        result = file + '.webp'
        return result.replace(str(media_path), '')
    else:
        return image_path.replace(str(media_path), '')
import cv2
import pytesseract
from PIL import Image
import numpy as np

# مسیر Tesseract را تنظیم کنید (در صورت نیاز)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # برای ویندوز


def preprocess_image(image_path):
    # خواندن تصویر
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # اعمال فیلترها برای بهبود کیفیت
    img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.medianBlur(img, 3)  # حذف نویز

    return img


def extract_persian_numbers(image_path):
    # پیش‌پردازش تصویر
    processed_img = preprocess_image(image_path)

    # تنظیمات Tesseract برای زبان فارسی
    custom_config = r'--oem 3 --psm 6 -l fas'

    # استخراج متن از تصویر
    text = pytesseract.image_to_string(processed_img, config=custom_config)

    # فیلتر کردن فقط اعداد فارسی
    persian_numbers = ''.join([char for char in text if char in '۰۱۲۳۴۵۶۷۸۹'])

    return persian_numbers


# تست کد
image_path = 'c:/captcha1.jpg'  # مسیر تصویر کپچا
result = extract_persian_numbers(image_path)
print("اعداد فارسی شناسایی‌شده:", result)
from django.test import TestCase
from app_hotel.models import Hotel
from app_crawl.kih.data import hotels

from distutils.command.clean import clean

import math


class DNS_mapping:
    list_hotels_kish = list()

    def __init__(self):
        # self.list_hotels_kish = list(Hotel.objects.all().values_list("name", flat=True))
        self.list_hotels_kish.append('تماشا')
        self.list_hotels_kish.append('سيمرغ')
        self.list_hotels_kish.append('ایران')
        self.list_hotels_kish.append('پانوراما')
        self.list_hotels_kish.append('کوروش')
        # self.list_hotels_kish.append('بين اللملي')
        self.list_hotels_kish.append('ليليوم')
        self.list_hotels_kish.append('بین المللی')
        self.list_hotels_kish.append('پارميس')
        self.list_hotels_kish.append('ترنج')
        self.list_hotels_kish.append('داريوش')
        self.list_hotels_kish.append('شايان')
        self.list_hotels_kish.append('شايگان')
        self.list_hotels_kish.append('مارينا پارک')
        self.list_hotels_kish.append('ميراژ')
        self.list_hotels_kish.append('سارا')
        self.list_hotels_kish.append('سورينت مريم')
        self.list_hotels_kish.append('سورينت صدف')
        self.list_hotels_kish.append('فلامينگو')
        self.list_hotels_kish.append('کاباناگاردن ارم')

        self.list_hotels_kish.append('ارم سوئيت محوطه')
        self.list_hotels_kish.append('لوتوس')
        self.list_hotels_kish.append('آرامش')
        self.list_hotels_kish.append('سان رايز')
        self.list_hotels_kish.append('سانرايز')
        self.list_hotels_kish.append('گراند')
        self.list_hotels_kish.append('گاردنيا')
        self.list_hotels_kish.append('آفتاب شرق')
        self.list_hotels_kish.append('پارس نيک')
        self.list_hotels_kish.append('پارسيان')
        self.list_hotels_kish.append('تعطيلات')
        self.list_hotels_kish.append('ريان قائم')
        self.list_hotels_kish.append('رویان')
        self.list_hotels_kish.append('آريان')
        self.list_hotels_kish.append('ريان')
        self.list_hotels_kish.append('شايلي')
        self.list_hotels_kish.append('گامبرون')
        self.list_hotels_kish.append('گلديس')
        self.list_hotels_kish.append('پانيذ')
        self.list_hotels_kish.append('خاتم')
        self.list_hotels_kish.append('آبادگران')
        self.list_hotels_kish.append('ققنوس')
        self.list_hotels_kish.append('آريان')
        self.list_hotels_kish.append('فانوس')
        self.list_hotels_kish.append('پارميدا')
        self.list_hotels_kish.append('شباويز')
        self.list_hotels_kish.append('جام جم')
        self.list_hotels_kish.append('هليا')
        # self.list_hotels_kish.append('ارم بزرگ')
        self.list_hotels_kish.append('ارم')
        self.list_hotels_kish.append('آراميس پلاس')
        self.list_hotels_kish.append('آراميس')
        self.list_hotels_kish.append('ویدا')
        self.list_hotels_kish.append('صدف')
        self.list_hotels_kish.append('پالاس')
        self.list_hotels_kish.append('اسپادانا')
        self.list_hotels_kish.append('آنا')
        self.list_hotels_kish.append('ستاره')
        for iter in range(0, len(self.list_hotels_kish)):
            self.list_hotels_kish[iter] = self.preprocess_text(self.list_hotels_kish[iter])

    def levenshtein_distance(self, s, t):
        m = len(s)
        n = len(t)
        d = [[0] * (n + 1) for i in range(m + 1)]
        for i in range(1, m + 1):
            d[i][0] = i
        for j in range(1, n + 1):
            d[0][j] = j
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                if s[i - 1] == t[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
        return d[m][n]

    def typeRoom(self, text, cleantext):
        if ('دبل' in text and ('تخت' not in text and 'نفر' not in text)):
            cleantext = 'دو تخت ' + cleantext
        if ('کانکت' in text):
            cleantext = 'کانکت ' + cleantext
        if ('کابانا' in text):
            cleantext = 'کابانا ' + cleantext

        return cleantext

    def check_servis(self, text):
        if ('سرویس' in text):
            text_pro = ''
            if ('با' in text):
                text_pro = text.split('با')[1]
            else:
                if ('+' in text):
                    text_pro = text.split('+')[1]

            if ('دو' in text_pro):
                return 2
            if ('سه' in text_pro):
                return 3
            if ('چهار' in text_pro):
                return 4
            if ('پنج' in text_pro):
                return 5
            if ('شش' in text_pro):
                return 6
            if ('هفت' in text_pro):
                return 7
            return 1
        else:
            return 0

    def takhtRoom(self, text, cleantext):
        tedad_ezafe = self.check_servis(text)

        if ('یک تخت' in text or 'یکتخت' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 1)) + 'تخت'

        if ('دو تخت' in text or 'دوتخت' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 2)) + 'تخت'

        if ('سه تخت' in text or 'سهتخت' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 3)) + 'تخت'
            # if ('با سرویس' in text or '+ سرویس اضافه' in text):
            #     cleantext = cleantext + " چهار تخت"
            # else:
            #     cleantext = cleantext + " سه تخت"
        if ('چهار تخت' in text or 'چهارتخت' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 4)) + 'تخت'
            # if ('با سرویس' in text or '+ سرویس اضافه' in text):
            #     cleantext = cleantext + " پنج تخت"
            # else:
            #     cleantext = cleantext + " چهار تخت"

        if ('پنج تخت' in text or 'پنجتخت' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 5)) + 'تخت'
            # if ('با سرویس' in text or '+ سرویس اضافه' in text):
            #     cleantext = cleantext + " شش تخت"
            # else:
            #     cleantext = cleantext + " پنج تخت"

        if ('شش تخت' in text or 'ششتخت' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 6)) + 'تخت'

        return cleantext

    def royalRoom(self, text, cleantext):
        if ('رویال' in text):
            cleantext = cleantext + " رویال";

        if ('تویین' in text or 'توئین' in text):
            cleantext = cleantext + " تویین";

        return cleantext;

    def robeRoom(self, text, cleantext):

        if (
                'رو به دریا' in text or 'روبه دریا' in text or
                'جهت دریا' in text or 'دریا' in text
        ):
            cleantext = cleantext + ' رو به دریا';

        if (
                'رو به غروب' in text or 'روبه غروب' in text or
                'جهت غروب' in text or 'غروب' in text
        ):
            cleantext = cleantext + ' رو به غروب';

        if (
                'رو به جزیره' in text or 'روبه جزیره' in text or
                'جهت جزیره' in text or 'جزیره' in text
        ):
            cleantext = cleantext + ' رو به جزیره';

        if (
                'رو به پارک' in text or 'روبه پارک' in text or
                'جهت پارک' in text or 'پارک' in text
        ):
            cleantext = cleantext + ' رو به پارک';

        if (
                'رو به باغ' in text or 'روبه باغ' in text or
                'جهت باغ' in text or 'باغ' in text
        ):
            cleantext = cleantext + ' رو به باغ';

        if (
                'رو به پردیس' in text or 'روبه پردیس' in text or
                'جهت پردیس' in text or 'پردیس' in text
        ):
            cleantext = cleantext + ' رو به پردیس';

        return cleantext;

    def loksRoom(self, text, cleantext):
        if ('VIP' in text or 'vip' in text):
            cleantext = cleantext + ' ويژه '
        if (' لوکس' in text or 'top' in text or ' لوکــــــس' in text):
            cleantext = cleantext + ' لوکس '
        if ('ویلایی' in text):
            cleantext = cleantext + ' ویلایی '

        if ('ممتاز' in text):
            cleantext = cleantext + ' ممتاز '
        if ('ویژه' in text):
            cleantext = cleantext + ' ويژه '

        return cleantext

    def naharRoom(self, text, cleantext):

        if ('نهار' in text or 'ناهار' in text):
            cleantext = cleantext + " با نهار "
        return cleantext

    def khabeRoom(self, text, cleantext):
        if ('یک خواب' in text or 'یکخواب' in text):
            cleantext = cleantext + ' يک خواب'
            return cleantext
        if ('دو خواب' in text or 'دوخواب' in text or 'دو خواب' in text):
            cleantext = cleantext + ' دو خواب'
            return cleantext
        if ('سه خواب' in text or 'سهخواب' in text):
            cleantext = cleantext + ' سه خواب'
            return cleantext
        if ('چهار خواب' in text or 'چهارخواب' in text):
            cleantext = cleantext + ' چهار خواب'
            return cleantext
        if ('پنج خواب' in text or 'پنجخواب' in text):
            cleantext = cleantext + ' پنج خواب'
            return cleantext

        return cleantext

    def nafareRoom(self, text, cleantext):
        tedad_ezafe = 0
        if ('تخت' not in text):
            tedad_ezafe = self.check_servis(text)

        if ('پنج نفر' in text or 'پنج  نفر' in text or 'پنجنفر' in text):
            # if ('پنج' in text and 'نفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 5)) + 'تخت'
            # cleantext = cleantext + ' پنج تخت'
            return cleantext

        # if  ('شش' in text and 'نفر' in text):
        if ('شش نفر' in text or 'شش  نفر' in text or 'ششنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 6)) + 'تخت'
            # cleantext = cleantext + ' پنج تخت'
            return cleantext

        # if  ('چهار' in text and 'نفر' in text):
        if ('چهار نفر' in text or 'چهار  نفر' in text or 'چهارنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 4)) + 'تخت'
            # cleantext = cleantext + ' چهار تخت'
            return cleantext

        # if  ('یک' in text and 'نفر' in text):
        if ('یک نفر' in text or 'یک  نفر' in text or 'یکنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 1)) + 'تخت'
            # cleantext = cleantext + ' یک تخت'
            return cleantext

        if ('دو نفر' in text or 'دو  نفر' in text or 'دونفر' in text):
            # if  ('دو' in text and 'نفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 2)) + 'تخت'
            # cleantext = cleantext + ' دو تخت'
            return cleantext

        # if  ('سه' in text and 'نفر' in text):
        if ('سه نفر' in text or 'سه  نفر' in text or 'سهنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 3)) + 'تخت'
            # cleantext = cleantext + ' سه تخت'
            return cleantext

        return cleantext

    def gheyreRoom(self, text, cleantext):

        if ('جونیور' in text or 'جورنیور' in text):
            cleantext = cleantext + ' جونیور'
        if ('ساحلی' in text):
            cleantext = cleantext + ' ساحلی'

        if ('ترنج' in text):
            cleantext = cleantext + ' ترنج'

        if ('دوبلکس' in text):
            cleantext = cleantext + ' دوبلکس'

        if ('پنت هوس' in text or 'پنت هاوس' in text):
            cleantext = cleantext + ' پنت هوس'

        if ('دلوکس' in text):
            cleantext = cleantext + ' دلوکس'

        if ('تراس دار' in text):
            cleantext = cleantext + ' تراس دار'

        if ('بالکن دار' in text):
            cleantext = cleantext + ' بالکن دار'

        if ('بدون تراس' in text):
            cleantext = cleantext + ' بدون تراس'
        if ('استودیو' in text):
            cleantext = cleantext + ' استودیو'
        if ('هافبرد' in text):
            cleantext = cleantext + ' هافبرد'
        if ('جکوزی دار' in text):
            cleantext = cleantext + ' جکوزی دار'
        if ('امپریال' in text):
            cleantext = cleantext + ' امپریال'

        if ('عروس و داماد' in text):
            cleantext = cleantext + ' عروس و داماد'

        if ('حمام سانروف' in text):
            cleantext = cleantext + ' حمام سانروف'

        if ('پرزیدنتال' in text):
            cleantext = cleantext + ' پرزیدنتال'

        if ('آتوسا' in text):
            cleantext = cleantext + ' آتوسا'

        if ('پانوراما' in text):
            cleantext = cleantext + ' پانوراما'

        return cleantext

    def create_standard(self, text):
        cleantext = ''
        # دبل
        cleantext = self.typeRoom(text, cleantext)
        cleantext = self.khabeRoom(text, cleantext)
        cleantext = self.takhtRoom(text, cleantext)
        cleantext = self.royalRoom(text, cleantext)
        cleantext = self.nafareRoom(text, cleantext)
        cleantext = self.robeRoom(text, cleantext)
        cleantext = self.loksRoom(text, cleantext)
        cleantext = self.naharRoom(text, cleantext)
        cleantext = self.gheyreRoom(text, cleantext)
        return cleantext

    def process_standardRoom(self, text):

        cleantext = self.create_standard(text)

        cleantext = 'اتاق ' + cleantext
        cleantext = cleantext.strip()
        cleantext = cleantext.replace('  ', ' ')
        return cleantext

    def process_sweetRoom(self, text):

        cleantext = self.create_standard(text)

        cleantext = "سوییت " + cleantext
        cleantext = cleantext.strip()
        cleantext = cleantext.replace("  ", " ")

        return cleantext

    def process_villaRoom(self, text):

        cleantext = self.create_standard(text)

        cleantext = "ویلا " + cleantext
        cleantext = cleantext.strip()
        cleantext = cleantext.replace("  ", " ")

        return cleantext

    def preprocess_text(self, text):
        text = text.replace("ـ", "")
        text = text.replace("ك", "ک")
        text = text.replace("دِ", "د")
        text = text.replace("بِ", "ب")
        text = text.replace("زِ", "ز")
        text = text.replace("شِ", "ش")
        text = text.replace("سِ", "س")
        text = text.replace("ى", "ی")
        text = text.replace("ي", "ی")
        text = text.replace("یــــــ", "ی")
        text = text.replace("ئ", "ی")
        text = text.replace("کـــــــ", "ک")
        text = text.replace("کــــــ", "ک")
        if ('تخت' in text):
            text = text.replace("سینگل", " ")
        else:
            text = text.replace("سینگل", "یک تخت")

        text = text.replace("١", "یک")
        text = text.replace("٢", "دو")
        text = text.replace("٣", "سه")
        text = text.replace("٤", "چهار")
        text = text.replace("٥", "پنج")
        text = text.replace("٦", "شش")
        text = text.replace("٧", "هفت")
        text = text.replace("٨", "هشت")
        text = text.replace("٩", "نه")
        text = text.replace("٠", "0")

        text = text.replace("1", " یک ")
        text = text.replace("2", " دو ")
        text = text.replace("3", " سه ")
        text = text.replace("4", " چهار ")
        text = text.replace("5", " پنج ")
        text = text.replace("6", " شش ")
        text = text.replace("7", " هفت")
        text = text.replace("8", " هشت ")
        text = text.replace("9", " نه ")

        text = text.replace("جزیـــــــره", " جزیره ")
        text = text.replace("پردیــــــس", " دریا ")
        text = text.replace("تاپ", " لوکس ")
        text = text.replace("غـــــــ", " غ ")
        text = text.replace("کانکـــــت", " کانکت ")
        text = text.replace("ناهــــــــــــار", " نهار ")
        text = text.replace("سوئیت", " سوییت ")
        text = text.replace("جزیزه", "جزیره")
        text = text.replace("سروریس", "سرویس")
        text = text.replace("پرزیدنشال", "پرزیدنتال")
        text = text.replace("twin", "توئین")
        return text

    def check_hotelName(self, text):

        text = self.preprocess_text(text)
        for i in range(0, len(self.list_hotels_kish)):
            spl = self.list_hotels_kish[i].split(' ')
            cnt = 0
            for j in range(0, len(spl)):
                if (spl[j] in text):
                    cnt = cnt + 1
            if (cnt == len(spl)):
                # if ('ارم' in text and
                #         'محوطه' not in text and
                #         'پارميدا' not in text and
                #         'پارميس' not in text and
                #         'کاباناگاردن ارم' not in text):
                if (' ارم' in text or
                    'ارم ' in text) and ('گاردن' not in text):
                    return 'هتل ' + self.list_hotels_kish[i] + ' بزرگ کیش'
                if ('صدف' in text and 'سورينت' not in text):
                    return 'هتل ' + 'سورينت صدف' + ' کیش'
                return 'هتل ' + self.list_hotels_kish[i] + ' کیش'

        # ==== Check with Levenstain =====

        # =======================
        maxx = math.inf
        matched = ''
        for item in self.list_hotels_kish:
            distance = self.levenshtein_distance(text, item)
            if (distance < maxx):
                matched = item
                maxx = distance

        # print(f"The Levenshtein distance between '{s1}' and '{matched}' is {distance}")
        # ====================
        return 'هتل ' + matched + ' کیش'
        # return matched

    def check_roomName(self, text):
        text = self.preprocess_text(text)
        # if ('(' in  text):
        #     text=text.split('(')[0]
        #     # return ""

        text = text.replace('  ', ' ')

        if ('اتاق یک تخت' in text):
            parsed = 'اتاق یک تخت'
            parsed = parsed.replace('  ', ' ')
            return parsed

        if ('سوییت' in text or 'سویت' in text):
            parsed = self.process_sweetRoom(text)
            parsed = parsed.replace('  ', ' ')
            return parsed

        if ('ویلا ' in text):
            parsed = self.process_villaRoom(text)
            parsed = parsed.replace('  ', ' ')
            return parsed

        # if ('سوییت' not in text or 'کانکت' not in text or 'کابانا' not in text):
        if ('سوییت' not in text):
            parsed = self.process_standardRoom(text)
            parsed = parsed.replace('  ', ' ')
            return parsed


class TestHotel(TestCase):
    def setUp(self) -> None:
        for hotel in list(hotels.keys()):
            hotel_name = hotel.replace("کیش", "")
            hotel_name = hotel_name.replace("هتل", "")
            hotel_name = hotel_name.strip()
            Hotel.objects.create(
                name=hotel_name,
                city_code="KIH"
            )

    def testMap(self):
        ds = DNS_mapping()
        print("--------------------------------------")
        print(F"{ds.list_hotels_kish = }")
        print("--------------------------------------")
        print(f'{ds.check_hotelName("کيش(5ستاره)====ایران") = }')
        print(f'{ds.check_hotelName("هلییا کیش") = }')
        print(f'{ds.check_hotelName("ارم کیش") = }')
        print(f'{ds.check_hotelName("ارم بزرگ کیش") = }')
        print(f'{ds.check_hotelName("کاباناگارن ارم کیش") = }')
        print(f'{ds.check_hotelName("ارامش کیش") = }')

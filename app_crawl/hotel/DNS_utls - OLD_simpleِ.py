from distutils.command.clean import clean
import re
import math
#=== Initialize ===========
import  json
with open('app_crawl/hotel/HotelRooms_Mojalal24_withStars2.json', 'r', encoding='utf-8') as json_file:
    HotelRooms = json.load(json_file)



mojalal_mashhadHotels=[a['hotelname'].replace('*','').strip() for a in HotelRooms if a['destination']=="مشهد"  and 'star' in a]
mojalal_TehranHotels=[a['hotelname'].replace('_','').strip() for a in HotelRooms if a['destination']=="تهران مهرآباد" and 'star' in a]
mojalal_yazdHotels=[a['hotelname'].replace('/','').strip() for a in HotelRooms if a['destination']=="يزد" and 'star' in a]
mojalal_IsfahanHotels=[a['hotelname'].replace('.','').strip() for a in HotelRooms if a['destination']=="اصفهان" and 'star' in a]
mojalal_shirazHotels=[a['hotelname'].replace('+','').strip() for a in HotelRooms if a['destination']=="شيراز" and 'star' in a]
mojalal_tabrizHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="تبريز" and 'star' in a]


mojalal_rashtHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="رشت" and 'star' in a]
mojalal_sariHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="ساري" and 'star' in a]
mojalal_kermanHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="کرمان" and 'star' in a]
mojalal_ChabaharHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="چابهار" and 'star' in a]
mojalal_KermanshahHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="کرمانشاه" and 'star' in a]
mojalal_BandarabasHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="بندرعباس" and 'star' in a]
mojalal_AhwazHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="اهواز" and 'star' in a]


mojalal_AbadanHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="آبادان" and 'star' in a]
mojalal_BooshehrHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="بوشهر" and 'star' in a]
mojalal_GorganHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="گرگان" and 'star' in a]
mojalal_OromiyeHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="اروميه" and 'star' in a]
mojalal_ArdebilHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="اردبيل" and 'star' in a]
mojalal_HamedanHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="همدان" and 'star' in a]
mojalal_RamsarHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="رامسر" and 'star' in a]
mojalal_KhorramAbadHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="خرم آباد" and 'star' in a]

mojalal_KishHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="کيش" and 'star' in a]
mojalal_GheshmHotels=[a['hotelname'].replace(':','').strip() for a in HotelRooms if a['destination']=="قشم" and 'star' in a]




mojalal_mashhadHotels_star=[a['star'] for a in HotelRooms if a['destination']=="مشهد" and 'star' in a]
mojalal_TehranHotels_star=[a['star'] for a in HotelRooms if a['destination']=="تهران مهرآباد" and 'star' in a]
mojalal_yazdHotels_star=[a['star'] for a in HotelRooms if a['destination']=="يزد" and 'star' in a]
mojalal_IsfahanHotels_star=[a['star'] for a in HotelRooms if a['destination']=="اصفهان" and 'star' in a]
mojalal_shirazHotels_star=[a['star'] for a in HotelRooms if a['destination']=="شيراز" and 'star' in a]
mojalal_tabrizHotels_star=[a['star'] for a in HotelRooms if a['destination']=="تبريز" and 'star' in a]

mojalal_rashtHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="رشت" and 'star' in a]
mojalal_sariHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="ساري" and 'star' in a]
mojalal_kermanHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="کرمان" and 'star' in a]
mojalal_ChabaharHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="چابهار" and 'star' in a]
mojalal_KermanshahHotels_star=[str(a.get('star', '')).replace(':','').strip() for a in HotelRooms if a['destination']=="کرمانشاه" and 'star' in a]
mojalal_BandarabasHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="بندرعباس" and 'star' in a]
mojalal_AhwazHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="اهواز" and 'star' in a]


mojalal_AbadanHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="آبادان" and 'star' in a]
mojalal_BooshehrHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="بوشهر" and 'star' in a]
mojalal_GorganHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="گرگان" and 'star' in a]
mojalal_OromiyeHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="اروميه" and 'star' in a]
mojalal_ArdebilHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="اردبيل" and 'star' in a]
mojalal_HamedanHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="همدان" and 'star' in a]
mojalal_RamsarHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="رامسر" and 'star' in a]
mojalal_KhorramAbadHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="خرم آباد" and 'star' in a]


mojalal_KishHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="کيش" and 'star' in a]
mojalal_GheshmHotels_star=[a['star'].replace(':','').strip() for a in HotelRooms if a['destination']=="قشم" and 'star' in a]

HotelRooms_mojalal={}

HotelRooms_mojalal['KIH']={
    'hotels': mojalal_KishHotels,
    'stars':mojalal_KishHotels_star
}

HotelRooms_mojalal['GSM']={
    'hotels': mojalal_GheshmHotels,
    'stars':mojalal_GheshmHotels_star
}


HotelRooms_mojalal['MHD']={
    'hotels': mojalal_mashhadHotels,
    'stars':mojalal_mashhadHotels_star
}
HotelRooms_mojalal['THR']={

    'hotels':mojalal_TehranHotels,
    'stars':mojalal_TehranHotels_star
}

HotelRooms_mojalal['AZD']={
    'hotels':mojalal_yazdHotels,
    'stars':mojalal_yazdHotels_star
}
HotelRooms_mojalal['IFN']={
    'hotels':mojalal_IsfahanHotels,
    'stars':mojalal_IsfahanHotels_star
}
HotelRooms_mojalal['SYZ']={
    'hotels':mojalal_shirazHotels,
    'stars':mojalal_shirazHotels_star
}
HotelRooms_mojalal['TBZ']={
    'hotels':mojalal_tabrizHotels,
    'stars':mojalal_tabrizHotels_star
}



HotelRooms_mojalal['AWZ']={
    'hotels':mojalal_AhwazHotels,
    'stars':mojalal_AhwazHotels_star
}

HotelRooms_mojalal['ZBR']={
    'hotels':mojalal_ChabaharHotels,
    'stars':mojalal_ChabaharHotels_star
}

HotelRooms_mojalal['KER']={
    'hotels':mojalal_kermanHotels,
    'stars':mojalal_kermanHotels_star
}

HotelRooms_mojalal['KSH']={
    'hotels':mojalal_KermanshahHotels,
    'stars':mojalal_KermanshahHotels_star
}

HotelRooms_mojalal['BND']={
    'hotels':mojalal_BandarabasHotels,
    'stars':mojalal_BandarabasHotels_star
}

HotelRooms_mojalal['RAS']={
    'hotels':mojalal_rashtHotels,
    'stars':mojalal_rashtHotels_star
}

HotelRooms_mojalal['SRY']={
    'hotels':mojalal_sariHotels,
    'stars':mojalal_sariHotels_star
}

HotelRooms_mojalal['ABD']={
    'hotels':mojalal_AbadanHotels,
    'stars':mojalal_AbadanHotels_star
}

HotelRooms_mojalal['BUZ']={
    'hotels':mojalal_BooshehrHotels,
    'stars':mojalal_BooshehrHotels_star
}

HotelRooms_mojalal['GBT']={
    'hotels':mojalal_GorganHotels,
    'stars':mojalal_GorganHotels_star
}

HotelRooms_mojalal['OMH']={
    'hotels':mojalal_OromiyeHotels,
    'stars':mojalal_OromiyeHotels_star
}

HotelRooms_mojalal['ADU']={
    'hotels':mojalal_ArdebilHotels,
    'stars':mojalal_ArdebilHotels_star
}

HotelRooms_mojalal['HDM']={
    'hotels':mojalal_HamedanHotels,
    'stars':mojalal_HamedanHotels_star
}

HotelRooms_mojalal['RZR']={
    'hotels':mojalal_RamsarHotels,
    'stars':mojalal_RamsarHotels_star
}


HotelRooms_mojalal['KHD']={
    'hotels':mojalal_KhorramAbadHotels,
    'stars':mojalal_KhorramAbadHotels_star
}


# value = "NSH" > نوشهر < / option > -->



mapping_name={
    'THR':'تهران',
    'MHD':'مشهد',
    'AZD':'یزد',
    'IFN':'اصفهان',
    'SYZ':'شیراز',
    'TBZ':'تبریز',
    'KIH':'کیش',
    'GSM':'قشم',
    'DXB':'دبی',
    'TR':'استانبول',



    'AWZ':'اهواز',
    'BND':'بندرعباس',
    'KER':'کرمان',
    'KSH':'کرمانشاه',
    'RAS':'رشت',
    'SRY':'ساری',
    'ZBR':'چابهار',


    'ABD':'ابادان',
    'BUZ':'بوشهر',
    'GBT':'گرگان',
    'OMH':'ارومیه',
    'ADU':'اردبیل',
    'HDM':'همدان',
    'RZR':'رامسر',
    'KHD':'خرم اباد',
    'NSH':'نوشهر',


    'KIH':'کیش',
    'GSM':'قشم',

}




#=====

class DNS_mapping:
    list_hotels_kish=list()
    list_hotels_ghesm=list()
    def __init__(self):

        #======== read GSM hotels
        with open(f'app_crawl/hotel/lst_GSM_hotels.txt', 'r', encoding='utf8') as fi:
            self.list_hotels_ghesm=fi.readlines()
            self.list_hotels_ghesm=[htl.replace('\n','').replace('هتل','').replace('قشم','').strip() for htl in self.list_hotels_ghesm]
        for iter in range(0,len(self.list_hotels_ghesm)):
            self.list_hotels_ghesm[iter]=self.preprocess_text(self.list_hotels_ghesm[iter])
        #================
        self.list_hotels_kish.append('تماشا')
        self.list_hotels_kish.append('سيمرغ')
        self.list_hotels_kish.append('ايران')
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
        for iter in range(0,len(self.list_hotels_kish)):
            self.list_hotels_kish[iter]=self.preprocess_text(self.list_hotels_kish[iter])

        #=========================================================================



    def levenshtein_distance(self,s, t):
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

    def typeRoom(self,text,cleantext):
        if ('دبل' in text and ('تخت' not in text and 'نفر' not in text)):
            cleantext='دو تخت '+cleantext
        if ('کانکت' in text):
            cleantext='کانکت '+cleantext
        if ('کابانا' in text):
            cleantext = 'کابانا ' + cleantext


        return cleantext

    def check_servis(self,text):
        if ('سرویس' in text):
            text_pro=''
            if ('با' in text):
                text_pro=text.split('با')[1]
            else:
                if ('+' in text):
                    text_pro=text.split('+')[1]

            
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
    def takhtRoom(self,text,cleantext):
        tedad_ezafe=self.check_servis(text)


        if ('یک تخت' in text or 'یکتخت' in text):
            cleantext = cleantext+' '+self.preprocess_text(str(tedad_ezafe+1))+'تخت'



        if ('دو تخت' in text or 'دوتخت' in text):
            cleantext = cleantext+' '+self.preprocess_text(str(tedad_ezafe+2))+'تخت'

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

    def royalRoom(self,text,cleantext):
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

    def loksRoom(self,text,cleantext):
        if ( 'VIP' in text or 'vip' in text):
            cleantext = cleantext + ' ويژه '
        if ( ' لوکس' in text or 'top' in text or ' لوکــــــس' in text):
            cleantext = cleantext + ' لوکس '
        if ('ویلایی' in text):
            cleantext = cleantext + ' ویلایی '

        if ('ممتاز' in text):
            cleantext = cleantext + ' ممتاز '
        if ('ویژه' in text):
            cleantext = cleantext + ' ويژه '

        return cleantext
    def naharRoom(self,text,cleantext):

        if ('نهار' in text or 'ناهار' in text):
                cleantext = cleantext + " با نهار "
        return cleantext

    def khabeRoom(self,text,cleantext):
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

    def nafareRoom(self,text,cleantext):
        tedad_ezafe=0
        if ('تخت' not in text):
            tedad_ezafe = self.check_servis(text)

        if ('پنج نفر' in text or 'پنج  نفر' in text or  'پنجنفر' in text):
        #if ('پنج' in text and 'نفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 5)) + 'تخت'
            # cleantext = cleantext + ' پنج تخت'
            return cleantext

        # if  ('شش' in text and 'نفر' in text):
        if ('شش نفر' in text or 'شش  نفر' in text or  'ششنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 6)) + 'تخت'
            # cleantext = cleantext + ' پنج تخت'
            return cleantext

        # if  ('چهار' in text and 'نفر' in text):
        if ('چهار نفر' in text or 'چهار  نفر' in text or  'چهارنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 4)) + 'تخت'
            # cleantext = cleantext + ' چهار تخت'
            return cleantext

        # if  ('یک' in text and 'نفر' in text):
        if ('یک نفر' in text or 'یک  نفر' in text or  'یکنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 1)) + 'تخت'
            # cleantext = cleantext + ' یک تخت'
            return cleantext

        if ('دو نفر' in text or 'دو  نفر' in text or  'دونفر' in text):
        # if  ('دو' in text and 'نفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 2)) + 'تخت'
            # cleantext = cleantext + ' دو تخت'
            return cleantext

        # if  ('سه' in text and 'نفر' in text):
        if ('سه نفر' in text or 'سه  نفر' in text or  'سهنفر' in text):
            cleantext = cleantext + ' ' + self.preprocess_text(str(tedad_ezafe + 3)) + 'تخت'
            # cleantext = cleantext + ' سه تخت'
            return cleantext

        return cleantext

    def gheyreRoom(self,text,cleantext):

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
    def create_standard(self,text):
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

    def process_standardRoom(self,text):

        cleantext=self.create_standard(text)

        cleantext = 'اتاق ' + cleantext
        cleantext = cleantext.strip()
        cleantext = cleantext.replace('  ', ' ')
        return cleantext



    def process_sweetRoom(self,text):

        cleantext = self.create_standard(text)

        cleantext = "سوییت " + cleantext
        cleantext = cleantext.strip()
        cleantext = cleantext.replace("  ", " ")

        return cleantext


    def process_villaRoom(self,text):

        cleantext = self.create_standard(text)

        cleantext = "ویلا " + cleantext
        cleantext = cleantext.strip()
        cleantext = cleantext.replace("  ", " ")

        return cleantext


    def preprocess_text(self,text):

        text=text.replace('آديينه','آدينه')
        text = text.replace("بوتیک", "").strip()
        if ('(' in text):
            text=text.split('(')[0]
        text=text.replace('آريا باستان ','آريا')
        text=text.replace('سورينت صدف ','صدف')



        text = text.replace(")", "")
        text = text.replace("(", "")
        text = text.replace("  ", " ")

        text = text.replace("ـ", "")
        text = text.replace("ك", "ک")
        text = text.replace("آ", "ا")
        text = text.replace("دِ", "د")
        text = text.replace("بِ", "ب")
        text = text.replace("زِ", "ز")
        text = text.replace("شِ", "ش")
        text = text.replace("سِ", "س")
        text = text.replace("ى", "ی")
        text = text.replace("ي", "ی")
        text = text.replace("ي", "ی")
        text = text.replace("ص", "ص")

        # Remove diacritics and unnecessary marks
        text = text.replace("ـ", "")  # Tatweel (kashida)
        text = text.replace("َ", "")  # Fatha
        text = text.replace("ً", "")  # Tanwin fatha
        text = text.replace("ِ", "")  # Kasra
        text = text.replace("ٍ", "")  # Tanwin kasra
        text = text.replace("ُ", "")  # Damma
        text = text.replace("ٌ", "")  # Tanwin damma
        text = text.replace("ْ", "")  # Sukun
        text = text.replace("ّ", "")  # Shadda

        # Normalize alphabetic variations
        text = text.replace("ك", "ک")  # Arabic Kaf to Persian Kaf
        text = text.replace("ي", "ی")  # Arabic Yeh to Persian Yeh
        text = text.replace("ى", "ی")  # Arabic Alif Maksura to Yeh
        text = text.replace("ة", "ه")  # Arabic Ta Marbuta to Heh
        text = text.replace("آ", "ا")  # Replace Alif Madda with Alif

        # Normalize common consonants with diacritics
        text = text.replace("دِ", "د")  # De with Kasra
        text = text.replace("بِ", "ب")  # Be with Kasra
        text = text.replace("زِ", "ز")  # Ze with Kasra
        text = text.replace("شِ", "ش")  # She with Kasra
        text = text.replace("سِ", "س")  # Se with Kasra

        # Additional Arabic letters that may have Persian equivalents
        text = text.replace("ؤ", "و")  # Waw with Hamza to Waw
        text = text.replace("ئ", "ی")  # Yeh with Hamza to Yeh
        text = text.replace("إ", "ا")  # Alif with Hamza below to Alif
        text = text.replace("أ", "ا")  # Alif with Hamza above to Alif

        # Additional replacements for Persian-specific characters
        text = text.replace("ں", "ن")  # Noon Ghunna to Noon
        text = text.replace("ۀ", "ه")  # Heh Doachashmee to Heh


        text = text.replace("یــــــ", "ی")
        text = text.replace("ئ", "ی")
        text = text.replace("کـــــــ", "ک")
        text = text.replace("کــــــ", "ک")
        if ( 'تخت' in text):
            text = text.replace("سینگل", " ")
        else:
            text = text.replace("سینگل", "یک تخت")

        arabic_to_persian = {
            '٠' '۰', '١' '۱', '٢' '۲', '٣' '۳', '٤' '۴',
            '٥' '۵', '٦' '۶', '٧' '۷', '٨' '۸', '٩' '۹'
        }
        english_to_persian = {
            '0' '۰', '1' '۱', '2' '۲', '3' '۳', '4' '۴',
            '5' '۵', '6' '۶', '7' '۷', '8' '۸', '9' '۹'
        }

        text = text.replace("۱", "یک")
        text = text.replace("۲", "دو")
        text = text.replace("۳", "سه")
        text = text.replace("۴", "چهار")
        text = text.replace("۵", "پنج")
        text = text.replace("۶", "شش")
        text = text.replace("۷", "هفت")
        text = text.replace("۸", "هشت")
        text = text.replace("۹", "نه")
        text = text.replace("۰", "0")

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

    def check_hotelName(self, text, destination):

        check_source = 'قصر الوند'
        check_DNS = 'قصر'
        step1 = False
        first_text = text

        if (first_text == check_source):
            print('sss')
            step1 = True

        # === for forien  destination
        if (
                destination == "DXB" or
                destination == "LON" or
                destination == "FRA" or
                destination == "YTO" or
                destination == "IST" or
                destination == "DOH"
        ):
            return text, '5'
        # =======
        # preprocess text
        #=========
        text = text.replace(')', ' ').replace('(', ' ')  # baraye text bayad ham dakhele parantese and kharej on biyad!
        text = self.preprocess_text(text).strip()
        text = text.split('-')[0]
        text = text.replace('هتل', ' ').strip()
        
        try:
            des = mapping_name.get(destination, destination)
            # if text.endswith(f" {des}"):
            #     text = text[:text.rfind(f" {des}")]
            if text.endswith(f"{des}"):
                text = text[:text.rfind(f"{des}")]
                text = text.strip()

        except:
            print('Destination Mapping Name Incorrect')
        # ===================

        #===========
        # Get All DNS
        #===========
        
        # ====== کلمه هتل و مقصد را برمیداریم =====
        lst_split = [

            'اقامتگاه بوم گردي',
            'اقامتگاه بوم گري',
            'اقامتگاه بومگردي',
            'اقامتگاه بوم‌گردی',
            'اقامتگاه بومگردی',

            'اقامتگاه سنتی',
            'اقامتگاه سنتي',
            'اقامتگاه سنتي خانه',
            'سرای سنتی',
            'سرای سنتی',

            # 'هتل سنتی',
            'هتل انتيک',
            'هتل موزه',
            # 'هتل سنتي',
            'سنتي',

            'لوکس',

            'کاروانسرای',
            'کاروان سرای',
            'کاروانسرا',
            'کاروان سرا',
            'مجتمع اقامتي',
            'مهمانپذير',

            'هاستل خانه مسافر',
            'هتل آپارتمان',

            'هتل',
            # 'خانه',
            # 'قصر',

            'توريستي',
            'اقامتی',
            'باغ ',
            'عمارت',

            'اقامتگاه',
            'بوتيک',
            'مجتمع',
            'مهمانپذير',

            'مهمانسراي',
            'مهمانسرا',
            'عمارت',
            'واحد اقامتي',
            'خانه مسافر',

            'بین المللی',
            'مجتمع گردشگری',
            'مجموعه گردشگری'
        ]

        sorted_lst_split = sorted(lst_split, key=len, reverse=True)
        lst_split = sorted_lst_split

        # === Check mojalal24 hotelNames =========
        lst_hotels_mojalal = HotelRooms_mojalal.get(destination, [])
        # Example list of hotel names you want to move to the end
        hotels_to_move_to_end = ["سنتی", "Hotel B", "Hotel C"]
        # Filter out hotels that need to be moved to the end
        regular_hotels = [
            (hotel, star)
            for hotel, star in zip(lst_hotels_mojalal['hotels'], lst_hotels_mojalal['stars'])
            if hotel not in hotels_to_move_to_end
        ]
        # Sort regular hotels by the length of hotel names in descending order
        sorted_regular_hotels = sorted(regular_hotels, key=lambda x: len(x[0]), reverse=True)
        # Gather the hotels that should be moved to the end
        end_hotels = [
            (hotel, star)
            for hotel, star in zip(lst_hotels_mojalal['hotels'], lst_hotels_mojalal['stars'])
            if hotel in hotels_to_move_to_end
        ]
        # Combine the sorted regular hotels with the hotels moved to the end
        sorted_pairs = sorted_regular_hotels + end_hotels
        # Unzip the sorted pairs back into separate lists for hotels and stars
        sorted_hotels, sorted_stars = zip(*sorted_pairs)
        # Convert to lists if needed
        sorted_hotels = list(sorted_hotels)
        sorted_stars = list(sorted_stars)
        lst_hotels_mojalal['hotels'] = list(sorted_hotels)
        lst_hotels_mojalal['stars'] = list(sorted_stars)

        # ====
        
        if (len(lst_hotels_mojalal) != 0):
            for i in range(0, len(lst_hotels_mojalal['hotels'])):
                
                #========
                # Preprocess dns_text
                #=======
                lst_hotels_mojalal['hotels'][i] = self.preprocess_text(lst_hotels_mojalal['hotels'][i])
                dns_text = lst_hotels_mojalal['hotels'][i].strip()

                dns_text = dns_text.replace('بندر عباس', 'بندرعباس')
                dns_text = dns_text.replace('پدرمن', 'پدر من')
                dns_text = dns_text.replace('دریادلان', 'دریا دلان')
                dns_text = dns_text.replace('دریاکنار ', 'دریا کنار ')
                dns_text = dns_text.replace('رویان قایم', 'ریان قایم')

                try:
                    des = mapping_name.get(destination, destination)
                    # if dns_text.endswith(f" {des}"):
                    #     dns_text = dns_text[:dns_text.rfind(f" {des}")]
                    if dns_text.endswith(f"{des}"):
                        dns_text = dns_text[:dns_text.rfind(f"{des}")]
                        dns_text = dns_text.strip()
                except:
                    print('Destination Mapping Name Incorrect')

                # --- split from هتل ----

                for s in lst_split:
                    s = self.preprocess_text(s)

                    # === سنتی ==== agar ba sonnati tamom mishavad! --> nabayad hazf shavad!!
                    if dns_text.endswith(f"{s}"):
                        continue
                    # ==========================
                    try:
                        s = s.strip()
                        dns_text = dns_text.split(s)[1].strip()
                        # break
                    except:
                        dns_text = dns_text.split(s)[0].strip()
                # ===============================

                # +========

                if (dns_text == ''):
                    continue

                dns_text = self.preprocess_text(dns_text)
                if (step1 and check_DNS in dns_text):
                    print('check DNS')
                # print(dns_text)

                # ================= استثنا ها =============
                if (destination == 'IFN' and text == "سوییت"):
                    text = self.preprocess_text('پارسیان سوییت')
                if (destination == 'AZD' and 'صفاییه' in text):
                    text = self.preprocess_text('پارسیان صفاییه')
                if (destination == 'AZD' and 'ارتیمیس' in text):
                    text = text.replace('ارتیمیس', 'ارتمیس')
                if (destination == 'SYZ'):
                    if (
                            text == 'اقا بابا خان' or
                            text == 'اقا باباخان' or
                            text == 'اقاباباخان' or
                            text == 'اقابابا خان'
                    ):
                        text = 'اقا باباخان'

                if (destination == 'AWZ' and 'امارانت' in text):
                    text = 'سومیا'

                if (destination == 'SRY' and 'سالار دره' in text):
                    text = 'سالاردره'

                if (destination == 'GBT' and 'قصر بوتانیک' in text):
                    text = 'قصربوتانیک'

                # =================

                text = ' ' + text + ' '
                spl = dns_text.split(' ')
                cnt = 0
                for j in range(0, len(spl)):
                    if (' ' + spl[j] + ' ' in text or
                            spl[j] + ' ' in text or
                            ' ' + spl[j] in text):
                        cnt = cnt + 1
                if (cnt == len(spl)):

                    # ==== Check hotel sonnati estefahn ======
                    if (dns_text == 'سنتی'):  # esme hotel mishavad yek sefat!!!!
                        if (len(text.strip().split(' ')) > 1):  # bayad word bishtarii nadashte bashad!!!1
                            continue
                    # ===================
                    return lst_hotels_mojalal['hotels'][i], lst_hotels_mojalal['stars'][i]
            # ========================================
        if text.strip() == '':
            return False, False
        return text, 'X'

    def check_roomName(self,text):
        text=self.preprocess_text(text)
        # if ('(' in  text):
        #     text=text.split('(')[0]
        #     # return ""

        text=text.replace('  ',' ')

        if ('اتاق یک تخت' in text):
            parsed='اتاق یک تخت'
            parsed=parsed.replace('  ',' ')
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
        # if ('سوییت' not in text):
        parsed=self.process_standardRoom(text)
        parsed = parsed.replace('  ', ' ')
        return parsed


#
# #--- test
# ds = DNS_mapping()
#
# # --- read result as Json
# import json
# # file='IFN__jsondata.json'
# # file='AWZ__jsondata.json'
# # file='SYZ__jsondata.json'
# # file='TBZ__jsondata.json'
# # file='AZD__jsondata.json'
# # file='AWZ__jsondata.json'
# # file='GBT__jsondata.json'
# # file='GSM__jsondata.json'
# # file='KIH__jsondata.json'
# # file='ADU__jsondata.json'
# # file='BND__jsondata.json'
# # file='BUZ__jsondata.json'
# # file='KER__jsondata.json'
# # file='KHD__jsondata.json'
# # file='KSH__jsondata.json'
# # file='OMH__jsondata.json'
# # file='RAS__jsondata.json'
#
# # file='RZR__jsondata.json'
# # file='SRY__jsondata.json'
# file='ZBR__jsondata.json'
#
#
#
#
# # BND
#
# fp = open(file,'r', encoding='utf8')
# readedd=fp.read()
# jsonData = json.loads(readedd)
# fp.close()
#
# fp1=open('natayej.txt','w',encoding='utf8')
# fp2=open('hotels_mande.txt','w',encoding='utf8')
#
# # --------
# # --
# for item in jsonData:
#     try:
#         hotel_name,hotel_star=ds.check_hotelName(item['hotel_name'], file.split('__')[0])
#         # print(hotel_star)
#         if (hotel_star=='X'):
#             fp1.write(f'{item["hotel_name"]}    --->  {hotel_name.strip()} \n')
#             fp2.write(f'{item["hotel_name"]}  \n' )
#             print(f'{item["hotel_name"]}    --->  {hotel_name.strip()}')
#     except:
#         continue
# fp1.close()
# fp2.close()
# #-------
# # #
# # # #====Main
# # ds=DNS_mapping()
# # htl_provider='ان کيش(5ستاره)====ایران'
# # htl_correct=ds.check_hotelName(htl_provider,'KIH')
# #
# # htl_provider='هتل آتامان قشم'
# # htl_correct=ds.check_hotelName(htl_provider,'GSM')
#
# # print(htl_correct)
# # #
# # room_provider='اتاق سه تخته لوکس روو به دریا'
# # room_provider='دو تخته دبل کابانا گاردن (هتل3ستاره)(اقامت صبحانه)'
# # room_provider='اتاق دو تخته'
# # room_provider='اتاق دبل استاندارد'
# # room_correct=ds.check_roomName(room_provider)
# # print(room_correct)
# from distutils.command.clean import clean
import copy
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
    # 'THR':'تهران',
    'THR':'تهران ',



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



# fp_test=open('test_hotel_DNS.txt','w',encoding='utf8')
#=====

class DNS_mapping:
    list_hotels_kish=list()
    list_hotels_ghesm=list()
    destination=''
    lst_hotels_mojalal=list()
    lst_hotels_mojalal_asli={}
    def __init__(self,destination):

        # #======== read GSM hotels
        # with open(f'lst_GSM_hotels.txt','r',encoding='utf8') as fi:
        #     self.list_hotels_ghesm=fi.readlines()
        #     self.list_hotels_ghesm=[htl.replace('\n','').replace('هتل','').replace('قشم','').strip() for htl in self.list_hotels_ghesm]
        # for iter in range(0,len(self.list_hotels_ghesm)):
        #     self.list_hotels_ghesm[iter]=self.preprocess_text(self.list_hotels_ghesm[iter])
        # #================
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


        #===========
        self.destination=destination
        self.ready_mojalal24_hotelnames()

        #===========
        ###?????????????????????????????????????????????????
        #=== Preprocess === ???????????============????????????================
        #
        # for iter in range(0,len(yazd_hotels)):
        #     yazd_hotels[iter]['title']=self.preprocess_text(yazd_hotels[iter]['title'])
        # for iter in range(0,len(gheshm_hotels)):
        #     gheshm_hotels[iter]['title']=self.preprocess_text(gheshm_hotels[iter]['title'])
        #
        # for iter in range(0,len(isfahan_hotels)):
        #     isfahan_hotels[iter]['title']=self.preprocess_text(isfahan_hotels[iter]['title'])
        #
        # for iter in range(0,len(kish_hotels)):
        #     kish_hotels[iter]['title']=self.preprocess_text(kish_hotels[iter]['title'])
        # for iter in range(0,len(mashhad_hotels)):
        #     mashhad_hotels[iter]['title']=self.preprocess_text(mashhad_hotels[iter]['title'])
        # for iter in range(0,len(shiraz_hotels)):
        #     shiraz_hotels[iter]['title']=self.preprocess_text(shiraz_hotels[iter]['title'])
        # for iter in range(0,len(tabriz_hotels)):
        #     tabriz_hotels[iter]['title']=self.preprocess_text(tabriz_hotels[iter]['title'])
        # for iter in range(0,len(tehran_hotels)):
        #     tehran_hotels[iter]['title']=self.preprocess_text(tehran_hotels[iter]['title'])
        #

        #=========================================================================


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

        if ('۸۵' not in text):
            text = text.replace("۵", "پنج")

        text = text.replace("۶", "شش")
        text = text.replace("۷", "هفت")

        if ('۸۵' not in text):
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

        if ('٨٥' not in text):
            text = text.replace("٥", "پنج")
        
        text = text.replace("٦", "شش")
        text = text.replace("٧", "هفت")

        if ('٨٥' not in text):
            text = text.replace("٨", "هشت")
        
        text = text.replace("٩", "نه")
        text = text.replace("٠", "0")

        text = text.replace("1", " یک ")
        text = text.replace("2", " دو ")
        text = text.replace("3", " سه ")
        text = text.replace("4", " چهار ")

        if ('85' not in text):
            text = text.replace("5", " پنج ")
        
        text = text.replace("6", " شش ")
        text = text.replace("7", " هفت")
        if ('85' not in text):
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

        text=text.replace("85","هشتاد و پنج")
        text=text.replace("هشتادوپنج","هشتاد و پنج")
        return text

    def ready_mojalal24_hotelnames(self):
        
        #=== Check mojalal24 hotelNames =========
        self.lst_hotels_mojalal=HotelRooms_mojalal.get(self.destination,[]).copy()


        # #===
        # # write lst_hotels_mojalal to file (test)
        # #===
        # fp3=open('lst_hotels_mojalal.txt','w',encoding='utf8')
        # for itemm in self.lst_hotels_mojalal['hotels']:
        #     fp3.write(itemm+'\n')
        # fp3.close()

        #-- write all HotelRooms_Mojalal24_withStars2.json hotels
        with open('app_crawl/hotel/HotelRooms_Mojalal24_withStars2.json','r',encoding='utf8') as fp:
            jsondata=fp.read()
            jsondata=json.loads(jsondata)
        lst_hotels_raw=[a['hotelname'] for a in jsondata]


        # fp3=open('HotelRooms_Mojalal24_withStars2_Hotelss.txt','w',encoding='utf8')
        # for itemm in lst_hotels_raw:
        #     fp3.write(itemm+'\n')
        # fp3.close()

        #========
        #-- sort lst_hotels_mojalal
        # lst_hotels_mojalal['hotels'].sort(key=len, reverse=True)

        #======= New Code
        # Example list of hotel names you want to move to the end
        hotels_to_move_to_end = ["سنتی", "Hotel B", "Hotel C"]

        # Filter out hotels that need to be moved to the end
        regular_hotels = [
            (hotel, star)
            for hotel, star in zip(self.lst_hotels_mojalal['hotels'], self.lst_hotels_mojalal['stars'])
            if hotel not in hotels_to_move_to_end
        ]

        # Sort regular hotels by the length of hotel names in descending order
        sorted_regular_hotels = sorted(regular_hotels, key=lambda x: len(x[0]), reverse=True)

        # Gather the hotels that should be moved to the end
        end_hotels = [
            (hotel, star)
            for hotel, star in zip(self.lst_hotels_mojalal['hotels'], self.lst_hotels_mojalal['stars'])
            if hotel in hotels_to_move_to_end
        ]

        # Combine the sorted regular hotels with the hotels moved to the end
        sorted_pairs = sorted_regular_hotels + end_hotels

        # Unzip the sorted pairs back into separate lists for hotels and stars
        sorted_hotels, sorted_stars = zip(*sorted_pairs)

        # Convert to lists if needed
        sorted_hotels = list(sorted_hotels)
        sorted_stars = list(sorted_stars)

        self.lst_hotels_mojalal['hotels'] = list(sorted_hotels)
        self.lst_hotels_mojalal['stars'] = list(sorted_stars)

        #====

        # self.lst_hotels_mojalal_asli = copy.deepcopy(self.lst_hotels_mojalal)
        self.lst_hotels_mojalal_asli = copy.deepcopy(self.lst_hotels_mojalal)
        
        original_index_map = {hotel: idx for idx, hotel in enumerate(self.lst_hotels_mojalal['hotels'])}

        # for item in lst_hotels_mojalal['hotels']:
        #     if ('هاتف' in item):
        #         print('ajab')



        import re
        if (len(self.lst_hotels_mojalal)!=0):
            for i in range(0,len(self.lst_hotels_mojalal['hotels'])):

                #========== NEW CODE ==========

                # if (self.lst_hotels_mojalal['hotels'][i]=="هتل آريا باستان کيش"):
                #     print('asdasdsad')


                if ('دار' in self.lst_hotels_mojalal['hotels'][i]):
                    print('asdasd')

                #===---------- NEW CODE -------------
                if ('سپیدار' in self.lst_hotels_mojalal['hotels'][i]):
                    print(' ')
                # print(dns_text)
                # fp_test.write(self.lst_hotels_mojalal['hotels'][i]+'\n')

                #----------------
                #======================




                self.lst_hotels_mojalal['hotels'][i]=self.preprocess_text(self.lst_hotels_mojalal['hotels'][i])

                dns_text = self.lst_hotels_mojalal['hotels'][i].strip()

                
                dns_text=dns_text.replace('بندر عباس','بندرعباس')
                dns_text=dns_text.replace('پدرمن','پدر من')
                dns_text=dns_text.replace('دریادلان','دریا دلان')
                dns_text=dns_text.replace('دریاکنار ','دریا کنار ')
                dns_text=dns_text.replace('رویان قایم','ریان قایم')
            
                
                try:
                    des = mapping_name.get(self.destination, self.destination).strip()
                    # if dns_text.endswith(f" {des}"):
                    #     dns_text = dns_text[:dns_text.rfind(f" {des}")]
                    if dns_text.endswith(f"{des}"):
                        dns_text = dns_text[:dns_text.rfind(f"{des}")]
                        dns_text=dns_text.strip()
                except:
                    print('Destination Mapping Name Incorrect')

                #====== کلمه هتل و مقصد را برمیداریم =====
                lst_split=[

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
                'مجلل',

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
                'مجموعه گردشگری',
                'مهمانپذر'
                    ]

                sorted_lst_split=sorted(lst_split,key=len,reverse=True)
                lst_split=sorted_lst_split

                # --- split from هتل ----

                for s in lst_split:
                    s=self.preprocess_text(s)

                    #=== سنتی ==== agar ba sonnati tamom mishavad! --> nabayad hazf shavad!!
                    if dns_text.endswith(f"{s}"):
                        continue
                    #==========================
                    try:
                        s=s.strip()
                        dns_text = dns_text.split(s)[1].strip()
                        # break
                    except:
                        dns_text = dns_text.split(s)[0].strip()
                #===============================





                #+========

                if (dns_text==''):
                    continue

                #== preprocess
                dns_text=self.preprocess_text(dns_text)


                # if (step1 and check_DNS in dns_text):
                #     print('check DNS')
                # print(dns_text)
                self.lst_hotels_mojalal['hotels'][i]=dns_text
        # fp_test.close()
        # return self.lst_hotels_mojalal_asli.copy()



        #=============================
        #============== NEW CODE (double code)=================
        #============================
        #== save temp
        dic_temp_listHotels={a : self.lst_hotels_mojalal_asli['hotels'][indx] for indx,a in enumerate(self.lst_hotels_mojalal['hotels'])}
        dic_temp_liststars={a : self.lst_hotels_mojalal_asli['stars'][indx] for indx,a in enumerate(self.lst_hotels_mojalal['hotels'])}
        

        #=== SORT again lst_hotels_mojalal
        combined = list(zip(self.lst_hotels_mojalal['hotels'], self.lst_hotels_mojalal['stars']))
        sorted_combined = sorted(combined, key=lambda x: len(x[0]), reverse=True)  # Sort by stars descending
        sorted_hotels, sorted_stars = zip(*sorted_combined)
        self.lst_hotels_mojalal['hotels'] = list(sorted_hotels)
        self.lst_hotels_mojalal['stars'] = list(sorted_stars)
                



        # Replace for lst_hotels_mojalal_asli
        lst_hotels_mojalal_asli2={}
        lst_hotels_mojalal_asli2['hotels']=[dic_temp_listHotels[a] for a in  self.lst_hotels_mojalal['hotels']]
        lst_hotels_mojalal_asli2['stars']=[dic_temp_liststars[a] for a in  self.lst_hotels_mojalal['hotels']]

        self.lst_hotels_mojalal_asli['hotels']=lst_hotels_mojalal_asli2['hotels']
        self.lst_hotels_mojalal_asli['stars']=lst_hotels_mojalal_asli2['stars']

       #==============================================



    def check_hotelName(self,text,destination):
        
        check_source='قصر الوند'
        check_DNS='قصر'
        step1=False
        first_text=text

        if (first_text==check_source):
            print('sss')
            step1=True

        #=== for forien  destination
        if (
                destination=="DXB" or
                destination=="LON" or
                destination=="FRA" or
                destination=="YTO" or
                destination=="IST" or
                destination=="DOH"
        ):


            return text,'5'
        #=======

        text=text.replace(')',' ').replace('(',' ')  # baraye text bayad ham dakhele parantese and kharej on biyad!

        text = self.preprocess_text(text)
        # print(text)
        if ('ایده ال' in text):
            print('asdsd')

        # 'بوتیک هتل ایده آل اردبیل'


        text = self.preprocess_text(text).strip()
        # print(text)
        # برای مشکل هتل کاروانیکا کرمان - کاروانسرای وکیل
        text=text.split('-')[0]

        text=text.replace('هتل',' ').strip()


        #============= برای هتل ستاره کیش ============
        if ('ستاره کیش' in text):
            text='ستاره'
        else:
            text=text.replace('ستاره','')

        #====================================


        try:


            des=mapping_name.get(destination, destination).strip()
            # if text.endswith(f" {des}"):
            #     text = text[:text.rfind(f" {des}")]

            if text.endswith(f"{des}"):
                text = text[:text.rfind(f"{des}")]
                text = text.strip()

        except:
            print('Destination Mapping Name Incorrect')
        #===================

        if (len(self.lst_hotels_mojalal)!=0):
            for i in range(0,len(self.lst_hotels_mojalal['hotels'])):

                dns_text = self.lst_hotels_mojalal['hotels'][i].strip()
                #================= استثنا ها =============
                if (destination=='IFN' and text=="سوییت"):
                    text=self.preprocess_text('پارسیان سوییت')
                if (destination=='AZD' and 'صفاییه' in text):
                    text=self.preprocess_text('پارسیان صفاییه')
                if (destination == 'AZD' and 'ارتیمیس' in text):
                    text = text.replace('ارتیمیس','ارتمیس')

                # if (destination=='GBT' and 'قصر بوتانیک')


                if (destination=='SYZ'):
                    if (
                            text=='اقا بابا خان' or
                            text=='اقا باباخان' or
                            text=='اقاباباخان' or
                            text=='اقابابا خان'
                    ):
                        text='اقا باباخان'


                if (destination=='AWZ' and 'امارانت' in text):
                    text='سومیا'

                if (destination=='SRY' and 'سالار دره' in text):
                    text='سالاردره'

                if (destination=='GBT' and 'قصر بوتانیک' in text):
                    text='قصربوتانیک'
                

                #=================


                text = ' ' + text + ' '
                spl=dns_text.split(' ')
                cnt=0
                for j in range(0,len(spl)):
                    if (' '+spl[j]+' ' in text or
                            spl[j]+' ' in text or
                            ' '+spl[j] in text):
                        cnt=cnt+1
                if(cnt==len(spl)):


                    #==== Check hotel sonnati estefahn ======
                    if (dns_text=='سنتی'): # esme hotel mishavad yek sefat!!!!
                        if (len(text.strip().split(' '))>1):  # bayad word bishtarii nadashte bashad!!!1
                            continue
                    #===================

                    #==== New Code ===
                    # if (text.strip()=='اریان'):
                    #     print('asdasdasdfvefr')

                    #+==
                    return self.lst_hotels_mojalal_asli['hotels'][i],self.lst_hotels_mojalal_asli['stars'][i]
            #========================================
        if text.strip()=='':
            return False,False
        return text,'X'




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
# #
# # # --- read result as Json
# # import json
# #
# #
# # # file='SYZ__jsondata.json'
# # # file='GBT__jsondata.json'
# # # file='ADU__jsondata.json'
# # # file='BND__jsondata.json'
# # # file='BUZ__jsondata.json'
# # # file='KSH__jsondata.json'
# # # file='RAS__jsondata.json'
# # # file='SRY__jsondata.json'
# # # file='ZBR__jsondata.json'
# # # file='ABD__jsondata.json'
# #
# #
# # #--------------
# # # file='RZR__jsondata.json'
# # # file='OMH__jsondata.json'
# # # file='KHD__jsondata.json'
# # # file='KER__jsondata.json'
# # # file='KIH__jsondata.json'
# # # file='AWZ__jsondata.json'
# # # file='AZD__jsondata.json'
# # # file='TBZ__jsondata.json'
# # # file='IFN__jsondata.json'
# #
# #
# #
# # # file='GSM__jsondata.json'
# # # file='THR__jsondata.json'
# file='KIH__jsondata_NEWWWWWW.json'
# #
# #
# # # BND
# # #--- test
# ds = DNS_mapping(file.split('__')[0])
# #
# #
# fp = open(file,'r', encoding='utf8')
# readedd=fp.read()
# jsonData = json.loads(readedd)
# fp.close()
#
# fp1=open('natayej.txt','w',encoding='utf8')
# fp2=open('hotels_mande.txt','w',encoding='utf8')
# #
# # # --------
# # # --
# import concurrent.futures
# def process_item(item, fp1, fp2, ds, file):
#     try:
#         # print(item['hotel_name'])
#         hotel_name, hotel_star = ds.check_hotelName(item['hotel_name'], file.split('__')[0])
#         # print(hotel_star)
#         if hotel_star == 'X':
#             fp1.write(f'{item["hotel_name"]}    --->  {hotel_name.strip()} \n')
#             fp2.write(f'{item["hotel_name"]}  \n')
#             # print(f'{item["hotel_name"]}    --->  {hotel_name.strip()}')
#     except Exception as e:
#         print(f"Error processing item: {item}. Error: {e}")
#
# def main(jsonData, fp1, fp2, ds, file):
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         futures = [
#             executor.submit(process_item, item, fp1, fp2, ds, file)
#             for item in jsonData
#         ]
#         concurrent.futures.wait(futures)
#     fp1.close()
#     fp2.close()
#
#
#
# main(jsonData, fp1, fp2, ds, file)


# # for item in jsonData:
# #     try:
# #         print(item['hotel_name'])
# #         hotel_name,hotel_star=ds.check_hotelName(item['hotel_name'], file.split('__')[0])
# #         # print(hotel_star)
# #         if (hotel_star=='X'):
# #             fp1.write(f'{item["hotel_name"]}    --->  {hotel_name.strip()} \n')
# #             fp2.write(f'{item["hotel_name"]}  \n' )
# #             print(f'{item["hotel_name"]}    --->  {hotel_name.strip()}')
# #     except:
# #         continue
# # fp1.close()
# # fp2.close()
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
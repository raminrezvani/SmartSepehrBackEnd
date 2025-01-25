from rest_framework import (status, )
from rest_framework.response import Response
from rest_framework.views import APIView
from app_crawl.cookie.get_cookie import (dayan_cookie, sepid_parvaz_cookie, mehrab_cookie, rahbal_cookie,
                                         tak_setareh_cookie, hrc_cookie, omid_oj_cookie, parmis_cookie, hamsafar_cookie,
                                         iman_cookie, flamingo_cookie, shayan_gasht_cookie, dolfin_cookie,
                                         yegane_fard_cookie, touristkish_cookie, eram2mhd_cookie, safiran_cookie,
                                         hamood_cookie, darvishi_cooke, moeindarbari_cooke)
from app_api.models import CookieProvider
from app_company.models import Provider, Company, CompanyAccountSign
from django.utils.timesince import timesince


def get_instance(code):
    if code == "dayan":
        return dayan_cookie
    elif code == "kimiya":
        return touristkish_cookie
    elif code == "eram2mhd":
        return eram2mhd_cookie
    elif code == "safiran":
        return safiran_cookie
    elif code == "hamood":
        return hamood_cookie


    elif code == "sepid_parvaz":
        return sepid_parvaz_cookie
    elif code == "mehrab":
        return mehrab_cookie
    elif code == "rahbal":
        return rahbal_cookie
    elif code == "tak_setareh":
        return tak_setareh_cookie
    elif code == "hrc":
        return hrc_cookie
    elif code == "omid_oj":
        return omid_oj_cookie
    elif code == "parmis":
        return parmis_cookie
    elif code == "hamsafar":
        return hamsafar_cookie
    elif code == "iman_amin":
        return iman_cookie
    elif code == "flamingo":
        return flamingo_cookie
    elif code == 'shayan_gasht':
        return shayan_gasht_cookie
    elif code == 'dolfin':
        return dolfin_cookie
    elif code == 'yegane_fard':
        return yegane_fard_cookie
    elif code == 'darvishi':
        return darvishi_cooke
    elif code == 'moeindarbari':
        return moeindarbari_cooke

    else:
        return dayan_cookie

from concurrent.futures import ThreadPoolExecutor
class SepehrCookieProviderAPI(APIView):
    def check_validity(self,instancec,provider_name,provider_code,has_sign,date):
        return instancec.get_validity(),provider_name,provider_code,has_sign,date


    def get(self, request):
        #===ramin
        executor=ThreadPoolExecutor(max_workers=10)
        threadResult=[]
        #===



        show_company = request.GET.get("show_company", "0")
        company_u_id = request.GET.get("company_u_id", None)
        check_has_sign = False
        # ---
        providers_result = []
        providers = Provider.objects.filter(soft_delete=False)
        # ---
        if company_u_id:
            qs_company = Company.objects.filter(soft_delete=False, u_id=company_u_id)
            if not qs_company:
                return Response(
                    {'message': "شرکتی یافت نشد"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            company = qs_company.last()
            check_has_sign = True
        # --- dayan
        for provider in providers:
            try:
                if check_has_sign:
                    date = timesince(CookieProvider.objects.filter(name=provider.code, company=company).last().date)
                else:
                    date = timesince(CookieProvider.objects.filter(name=provider.code).last().date)
                date = date.replace("days", "روز")
                date = date.replace("day", "روز")
                date = date.replace("hours", "ساعت")
                date = date.replace("hour", "ساعت")
                date = date.replace("minutes", "دقیقه")
                date = date.replace("minute", "دقیقه")
                date = date.replace("seconds", "ثانیه")
                date = date.replace("second", "ثانیه")
            except:
                date = "0"
            # ---
            instance = get_instance(provider.code)
            # ---
            if check_has_sign:
                qs_sign = CompanyAccountSign.objects.filter(soft_delete=False, provider=provider, company=company)
                if qs_sign.exists():
                    has_sign = True
                else:
                    has_sign = False
            else:
                has_sign = False
            # ---

            #===ramin
            threadResult.append(executor.submit(self.check_validity,instance,provider.name,provider.code,has_sign,date))
            #======
            # providers_result.append({
            #     "name": provider.name,
            #     "code": provider.code,
            #     "valid": instance.get_validity(),
            #     # "valid": True,
            #     "has_sign": has_sign,
            #     "date": date
            # })

        #====ramin
        for  th in threadResult:
            validity,provider_name, provider_code, has_sign, date=th.result()
            providers_result.append({
                "name": provider_name,
                "code": provider_code,
                "valid": validity,
                # "valid": True,
                "has_sign": has_sign,
                "date": date
            })
        #====-===
        # ---
        if show_company == "1":
            result = {
                "providers": providers_result,
                "companies": Company.objects.filter(soft_delete=False).values("u_id", "name")
            }
        else:
            result = providers_result
        # ---
        return Response(
            result,
            status=status.HTTP_200_OK
        )


class SepehrCookieAPI(APIView):
    def get(self, request):
        sepehr_name = request.GET.get("sepehr_name", None)
        sepehr_name = sepehr_name.lower()
        # ---
        instance = get_instance(sepehr_name)
        image = instance.get_captcha_image()
        # ---
        return Response(
            {'image': image},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        # --- request body
        try:
            sepehr_name = request.data['sepehr_name']
            company = request.data['company']
            recaptcha_code = request.data['recaptcha_code']
        except:
            return Response(
                {"message": "request body is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # ---
        qs_company = Company.objects.filter(soft_delete=False, u_id=company)
        if not qs_company:
            return Response(
                {"message": "company not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        company = qs_company.last()
        # ---
        if sepehr_name == "safiran":

            # # ==== Retrieve from Redis ========
            # if (safiran_cookie.GetCookie_FromDB(provider="safiran")):
            #     return True
            # # =====================================

            safiran_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="safiran", company=company)
            safiran_cookie.get_tour_cookie(target="KIH")
            safiran_cookie.get_tour_cookie(target="GSM")
            safiran_cookie.get_tour_cookie(target="SYZ")
            safiran_cookie.get_tour_cookie(target="MHD",SourceMabda="THR")  # baraye ashhad

            safiran_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            safiran_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            safiran_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            safiran_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad




            safiran_cookie.get_hotel_cookie(target='KIH')
            safiran_cookie.get_hotel_cookie(target='GSM')
            safiran_cookie.get_hotel_cookie(target='SYZ')
            safiran_cookie.get_hotel_cookie(target='MHD')
            safiran_cookie.get_hotel_cookie(target='THR')
            safiran_cookie.get_hotel_cookie(target='IFN')
            safiran_cookie.get_hotel_cookie(target='AZD')
            safiran_cookie.get_hotel_cookie(target='TBZ')


            safiran_cookie.get_hotel_cookie(target='AWZ')
            safiran_cookie.get_hotel_cookie(target='BND')
            safiran_cookie.get_hotel_cookie(target='ZBR')
            safiran_cookie.get_hotel_cookie(target='KER')
            safiran_cookie.get_hotel_cookie(target='KSH')
            safiran_cookie.get_hotel_cookie(target='RAS')
            safiran_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            safiran_cookie.insertCookie_intoDB(provider="safiran")
            # --------------------

            # safiran_cookie.get_hotel_cookie(target="GSM")
            safiran_cookie.close_driver()



        elif sepehr_name == "darvishi":
            #
            # # ==== Retrieve from Redis ========
            # if (darvishi_cooke.GetCookie_FromDB(provider="darvishi")):
            #     return True
            # # =====================================


            darvishi_cooke.login_sepehr(recaptcha_value=recaptcha_code, provider_code="darvishi", company=company)
            darvishi_cooke.get_tour_cookie(target="KIH")
            darvishi_cooke.get_tour_cookie(target="GSM")
            darvishi_cooke.get_tour_cookie(target="SYZ")
            darvishi_cooke.get_tour_cookie(target="MHD",SourceMabda="THR")  # baraye ashhad

            darvishi_cooke.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            darvishi_cooke.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            darvishi_cooke.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            darvishi_cooke.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            darvishi_cooke.get_hotel_cookie(target='KIH')
            darvishi_cooke.get_hotel_cookie(target='GSM')
            darvishi_cooke.get_hotel_cookie(target='SYZ')
            darvishi_cooke.get_hotel_cookie(target='MHD')
            darvishi_cooke.get_hotel_cookie(target='THR')
            darvishi_cooke.get_hotel_cookie(target='IFN')
            darvishi_cooke.get_hotel_cookie(target='AZD')
            darvishi_cooke.get_hotel_cookie(target='TBZ')


            darvishi_cooke.get_hotel_cookie(target='AWZ')
            darvishi_cooke.get_hotel_cookie(target='BND')
            darvishi_cooke.get_hotel_cookie(target='ZBR')
            darvishi_cooke.get_hotel_cookie(target='KER')
            darvishi_cooke.get_hotel_cookie(target='KSH')
            darvishi_cooke.get_hotel_cookie(target='RAS')
            darvishi_cooke.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            darvishi_cooke.insertCookie_intoDB(provider="darvishi")
            # --------------------

            # hamood_cookie.get_hotel_cookie(target="GSM")
            darvishi_cooke.close_driver()


        elif sepehr_name == "moeindarbari":

            # # ==== Retrieve from Redis ========
            # if (moeindarbari_cooke.GetCookie_FromDB(provider="moeindarbari")):
            #     return True
            # # =====================================


            moeindarbari_cooke.login_sepehr(recaptcha_value=recaptcha_code, provider_code="moeindarbari", company=company)
            moeindarbari_cooke.get_tour_cookie(target="KIH")
            moeindarbari_cooke.get_tour_cookie(target="GSM")
            moeindarbari_cooke.get_tour_cookie(target="SYZ")
            moeindarbari_cooke.get_tour_cookie(target="MHD",SourceMabda="THR")  # baraye ashhad

            moeindarbari_cooke.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            moeindarbari_cooke.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            moeindarbari_cooke.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            moeindarbari_cooke.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            moeindarbari_cooke.get_hotel_cookie(target='KIH')
            moeindarbari_cooke.get_hotel_cookie(target='GSM')
            moeindarbari_cooke.get_hotel_cookie(target='SYZ')
            moeindarbari_cooke.get_hotel_cookie(target='MHD')
            moeindarbari_cooke.get_hotel_cookie(target='THR')
            moeindarbari_cooke.get_hotel_cookie(target='IFN')
            moeindarbari_cooke.get_hotel_cookie(target='AZD')
            moeindarbari_cooke.get_hotel_cookie(target='TBZ')


            moeindarbari_cooke.get_hotel_cookie(target='AWZ')
            moeindarbari_cooke.get_hotel_cookie(target='BND')
            moeindarbari_cooke.get_hotel_cookie(target='ZBR')
            moeindarbari_cooke.get_hotel_cookie(target='KER')
            moeindarbari_cooke.get_hotel_cookie(target='KSH')
            moeindarbari_cooke.get_hotel_cookie(target='RAS')
            moeindarbari_cooke.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            moeindarbari_cooke.insertCookie_intoDB(provider="moeindarbari")
            # --------------------

            # hamood_cookie.get_hotel_cookie(target="GSM")
            moeindarbari_cooke.close_driver()





        elif sepehr_name == "hamood":

            # # ==== Retrieve from Redis ========
            # if (hamood_cookie.GetCookie_FromDB(provider="hamood")):
            #     return True
            # # =====================================


            hamood_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="hamood", company=company)
            hamood_cookie.get_tour_cookie(target="KIH")
            hamood_cookie.get_tour_cookie(target="GSM")
            hamood_cookie.get_tour_cookie(target="SYZ")
            hamood_cookie.get_tour_cookie(target="MHD",SourceMabda="THR")  # baraye ashhad

            hamood_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            hamood_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            hamood_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            hamood_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            hamood_cookie.get_hotel_cookie(target='KIH')
            hamood_cookie.get_hotel_cookie(target='GSM')
            hamood_cookie.get_hotel_cookie(target='SYZ')
            hamood_cookie.get_hotel_cookie(target='MHD')
            hamood_cookie.get_hotel_cookie(target='THR')
            hamood_cookie.get_hotel_cookie(target='IFN')
            hamood_cookie.get_hotel_cookie(target='AZD')
            hamood_cookie.get_hotel_cookie(target='TBZ')


            hamood_cookie.get_hotel_cookie(target='AWZ')
            hamood_cookie.get_hotel_cookie(target='BND')
            hamood_cookie.get_hotel_cookie(target='ZBR')
            hamood_cookie.get_hotel_cookie(target='KER')
            hamood_cookie.get_hotel_cookie(target='KSH')
            hamood_cookie.get_hotel_cookie(target='RAS')
            hamood_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            hamood_cookie.insertCookie_intoDB(provider="hamood")
            # --------------------

            # hamood_cookie.get_hotel_cookie(target="GSM")
            hamood_cookie.close_driver()


        # ---
        elif sepehr_name == "dayan":

            # # ==== Retrieve from Redis ========
            # if (dayan_cookie.GetCookie_FromDB(provider="dayan")):
            #     return True
            # # =====================================


            dayan_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="dayan", company=company)
            dayan_cookie.get_tour_cookie(target="KIH")
            dayan_cookie.get_tour_cookie(target="GSM")
            dayan_cookie.get_tour_cookie(target="SYZ")
            dayan_cookie.get_tour_cookie(target="MHD",SourceMabda="THR")  # baraye ashhad


            dayan_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            dayan_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            dayan_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            dayan_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad

            dayan_cookie.get_hotel_cookie(target='KIH')
            dayan_cookie.get_hotel_cookie(target='GSM')
            dayan_cookie.get_hotel_cookie(target='SYZ')
            dayan_cookie.get_hotel_cookie(target='MHD')
            dayan_cookie.get_hotel_cookie(target='THR')
            dayan_cookie.get_hotel_cookie(target='IFN')
            dayan_cookie.get_hotel_cookie(target='AZD')
            dayan_cookie.get_hotel_cookie(target='TBZ')


            dayan_cookie.get_hotel_cookie(target='AWZ')
            dayan_cookie.get_hotel_cookie(target='BND')
            dayan_cookie.get_hotel_cookie(target='ZBR')
            dayan_cookie.get_hotel_cookie(target='KER')
            dayan_cookie.get_hotel_cookie(target='KSH')
            dayan_cookie.get_hotel_cookie(target='RAS')
            dayan_cookie.get_hotel_cookie(target='SRY')



            # ---- insert into DB
            dayan_cookie.insertCookie_intoDB(provider="dayan")
            # --------------------


            # dayan_cookie.get_hotel_cookie()
            dayan_cookie.close_driver()


        elif sepehr_name == "kimiya":


            # # ==== Retrieve from Redis ========
            # if (touristkish_cookie.GetCookie_FromDB(provider="kimiya")):
            #     return True
            # # =====================================


            touristkish_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="kimiya", company=company)
            touristkish_cookie.get_tour_cookie(target="KIH")
            touristkish_cookie.get_tour_cookie(target="GSM")
            touristkish_cookie.get_tour_cookie(target="SYZ")
            touristkish_cookie.get_tour_cookie(target="MHD",SourceMabda="THR")  # baraye ashhad


            touristkish_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            touristkish_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            touristkish_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            touristkish_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad




            touristkish_cookie.get_hotel_cookie(target='KIH')
            touristkish_cookie.get_hotel_cookie(target='GSM')
            touristkish_cookie.get_hotel_cookie(target='SYZ')
            touristkish_cookie.get_hotel_cookie(target='MHD')
            touristkish_cookie.get_hotel_cookie(target='THR')
            touristkish_cookie.get_hotel_cookie(target='IFN')
            touristkish_cookie.get_hotel_cookie(target='AZD')
            touristkish_cookie.get_hotel_cookie(target='TBZ')


            touristkish_cookie.get_hotel_cookie(target='AWZ')
            touristkish_cookie.get_hotel_cookie(target='BND')
            touristkish_cookie.get_hotel_cookie(target='ZBR')
            touristkish_cookie.get_hotel_cookie(target='KER')
            touristkish_cookie.get_hotel_cookie(target='KSH')
            touristkish_cookie.get_hotel_cookie(target='RAS')
            touristkish_cookie.get_hotel_cookie(target='SRY')

            touristkish_cookie.insertCookie_intoDB(provider="kimiya")

            # touristkish_cookie.get_hotel_cookie()
            touristkish_cookie.close_driver()


        elif sepehr_name == "eram2mhd":


            # # ==== Retrieve from Redis ========
            # if (eram2mhd_cookie.GetCookie_FromDB(provider="eram2mhd")):
            #     return True


            eram2mhd_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="eram2mhd", company=company)
            eram2mhd_cookie.get_tour_cookie(target="KIH")

            eram2mhd_cookie.get_tour_cookie(target="KIH")
            eram2mhd_cookie.get_tour_cookie(target="GSM")
            eram2mhd_cookie.get_tour_cookie(target="SYZ")
            eram2mhd_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            eram2mhd_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            eram2mhd_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            eram2mhd_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            eram2mhd_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            eram2mhd_cookie.get_hotel_cookie(target='KIH')
            eram2mhd_cookie.get_hotel_cookie(target='GSM')
            eram2mhd_cookie.get_hotel_cookie(target='SYZ')
            eram2mhd_cookie.get_hotel_cookie(target='MHD')
            eram2mhd_cookie.get_hotel_cookie(target='THR')
            eram2mhd_cookie.get_hotel_cookie(target='IFN')
            eram2mhd_cookie.get_hotel_cookie(target='AZD')
            eram2mhd_cookie.get_hotel_cookie(target='TBZ')


            eram2mhd_cookie.get_hotel_cookie(target='AWZ')
            eram2mhd_cookie.get_hotel_cookie(target='BND')
            eram2mhd_cookie.get_hotel_cookie(target='ZBR')
            eram2mhd_cookie.get_hotel_cookie(target='KER')
            eram2mhd_cookie.get_hotel_cookie(target='KSH')
            eram2mhd_cookie.get_hotel_cookie(target='RAS')
            eram2mhd_cookie.get_hotel_cookie(target='SRY')

            eram2mhd_cookie.insertCookie_intoDB(provider="eram2mhd")



            # eram2mhd_cookie.get_hotel_cookie()
            eram2mhd_cookie.close_driver()



        elif sepehr_name == "sepid_parvaz":

            # # ==== Retrieve from Redis ========
            # if (sepid_parvaz_cookie.GetCookie_FromDB(provider="sepid_parvaz")):
            #     return True


            sepid_parvaz_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="sepid_parvaz",
                                             company=company)

            sepid_parvaz_cookie.get_tour_cookie(target="KIH")
            sepid_parvaz_cookie.get_tour_cookie(target="GSM")
            sepid_parvaz_cookie.get_tour_cookie(target="SYZ")
            sepid_parvaz_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad


            sepid_parvaz_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            sepid_parvaz_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            sepid_parvaz_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            sepid_parvaz_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad


            sepid_parvaz_cookie.get_hotel_cookie(target='KIH')
            sepid_parvaz_cookie.get_hotel_cookie(target='GSM')
            sepid_parvaz_cookie.get_hotel_cookie(target='SYZ')
            sepid_parvaz_cookie.get_hotel_cookie(target='MHD')
            sepid_parvaz_cookie.get_hotel_cookie(target='THR')
            sepid_parvaz_cookie.get_hotel_cookie(target='IFN')
            sepid_parvaz_cookie.get_hotel_cookie(target='AZD')
            sepid_parvaz_cookie.get_hotel_cookie(target='TBZ')


            sepid_parvaz_cookie.get_hotel_cookie(target='AWZ')
            sepid_parvaz_cookie.get_hotel_cookie(target='BND')
            sepid_parvaz_cookie.get_hotel_cookie(target='ZBR')
            sepid_parvaz_cookie.get_hotel_cookie(target='KER')
            sepid_parvaz_cookie.get_hotel_cookie(target='KSH')
            sepid_parvaz_cookie.get_hotel_cookie(target='RAS')
            sepid_parvaz_cookie.get_hotel_cookie(target='SRY')


            sepid_parvaz_cookie.insertCookie_intoDB(provider="sepid_parvaz")

            # sepid_parvaz_cookie.get_hotel_cookie()
            sepid_parvaz_cookie.close_driver()
        elif sepehr_name == "mehrab":

            # # ==== Retrieve from Redis ========
            # if (mehrab_cookie.GetCookie_FromDB(provider="mehrab")):
            #     return True

            mehrab_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="mehrab", company=company)
            mehrab_cookie.get_tour_cookie(target="KIH")
            mehrab_cookie.get_tour_cookie(target="GSM")
            mehrab_cookie.get_tour_cookie(target="SYZ")
            mehrab_cookie.get_tour_cookie(target="MHD",SourceMabda="THR")  # baraye ashhad

            mehrab_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            mehrab_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            mehrab_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            mehrab_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            mehrab_cookie.get_hotel_cookie(target='KIH')
            mehrab_cookie.get_hotel_cookie(target='GSM')
            mehrab_cookie.get_hotel_cookie(target='SYZ')
            mehrab_cookie.get_hotel_cookie(target='MHD')
            mehrab_cookie.get_hotel_cookie(target='THR')
            mehrab_cookie.get_hotel_cookie(target='IFN')
            mehrab_cookie.get_hotel_cookie(target='AZD')
            mehrab_cookie.get_hotel_cookie(target='TBZ')


            mehrab_cookie.get_hotel_cookie(target='AWZ')
            mehrab_cookie.get_hotel_cookie(target='BND')
            mehrab_cookie.get_hotel_cookie(target='ZBR')
            mehrab_cookie.get_hotel_cookie(target='KER')
            mehrab_cookie.get_hotel_cookie(target='KSH')
            mehrab_cookie.get_hotel_cookie(target='RAS')
            mehrab_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            mehrab_cookie.insertCookie_intoDB(provider="mehrab")

            # mehrab_cookie.get_hotel_cookie()
            mehrab_cookie.close_driver()
        elif sepehr_name == "rahbal":

            # # ==== Retrieve from Redis ========
            # if (rahbal_cookie.GetCookie_FromDB(provider="rahbal")):
            #     return True


            rahbal_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="rahbal", company=company)
            rahbal_cookie.get_tour_cookie(target="KIH")
            rahbal_cookie.get_tour_cookie(target="GSM")
            rahbal_cookie.get_tour_cookie(target="SYZ")
            rahbal_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad


            rahbal_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            rahbal_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            rahbal_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            rahbal_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            rahbal_cookie.get_hotel_cookie(target='KIH')
            rahbal_cookie.get_hotel_cookie(target='GSM')
            rahbal_cookie.get_hotel_cookie(target='SYZ')
            rahbal_cookie.get_hotel_cookie(target='MHD')
            rahbal_cookie.get_hotel_cookie(target='THR')
            rahbal_cookie.get_hotel_cookie(target='IFN')
            rahbal_cookie.get_hotel_cookie(target='AZD')
            rahbal_cookie.get_hotel_cookie(target='TBZ')

            rahbal_cookie.get_hotel_cookie(target='AWZ')
            rahbal_cookie.get_hotel_cookie(target='BND')
            rahbal_cookie.get_hotel_cookie(target='ZBR')
            rahbal_cookie.get_hotel_cookie(target='KER')
            rahbal_cookie.get_hotel_cookie(target='KSH')
            rahbal_cookie.get_hotel_cookie(target='RAS')
            rahbal_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            rahbal_cookie.insertCookie_intoDB(provider="rahbal")

            # rahbal_cookie.get_hotel_cookie()
            rahbal_cookie.close_driver()
        elif sepehr_name == "tak_setareh":


            # # ==== Retrieve from Redis ========
            # if (tak_setareh_cookie.GetCookie_FromDB(provider="tak_setareh")):
            #     return True
            # # =====================================


            # =====================================



            tak_setareh_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="tak_setareh",
                                            company=company)


            tak_setareh_cookie.get_tour_cookie(target="KIH")
            tak_setareh_cookie.get_tour_cookie(target="GSM")
            tak_setareh_cookie.get_tour_cookie(target="SYZ")
            tak_setareh_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            tak_setareh_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            tak_setareh_cookie.get_tour_cookie(target="IFN", SourceMabda="THR") # baraye ashhad
            tak_setareh_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            tak_setareh_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR") # baraye ashhad






            tak_setareh_cookie.get_hotel_cookie(target='KIH')
            tak_setareh_cookie.get_hotel_cookie(target='GSM')
            tak_setareh_cookie.get_hotel_cookie(target='SYZ')
            tak_setareh_cookie.get_hotel_cookie(target='MHD')
            tak_setareh_cookie.get_hotel_cookie(target='THR')
            tak_setareh_cookie.get_hotel_cookie(target='IFN')
            tak_setareh_cookie.get_hotel_cookie(target='AZD')
            tak_setareh_cookie.get_hotel_cookie(target='TBZ')


            tak_setareh_cookie.get_hotel_cookie(target='AWZ')
            tak_setareh_cookie.get_hotel_cookie(target='BND')
            tak_setareh_cookie.get_hotel_cookie(target='ZBR')
            tak_setareh_cookie.get_hotel_cookie(target='KER')
            tak_setareh_cookie.get_hotel_cookie(target='KSH')
            tak_setareh_cookie.get_hotel_cookie(target='RAS')
            tak_setareh_cookie.get_hotel_cookie(target='SRY')

            # ---- insert into DB
            tak_setareh_cookie.insertCookie_intoDB(provider="tak_setareh")
            # --------------------

            # tak_setareh_cookie.get_hotel_cookie()
            tak_setareh_cookie.close_driver()
        elif sepehr_name == "hrc":

            # # ==== Retrieve from Redis ========
            # if (hrc_cookie.GetCookie_FromDB(provider="hrc")):
            #     return True



            hrc_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="hrc", company=company)



            hrc_cookie.get_tour_cookie(target="KIH")
            hrc_cookie.get_tour_cookie(target="GSM")
            hrc_cookie.get_tour_cookie(target="SYZ")
            hrc_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad


            hrc_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            hrc_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            hrc_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            hrc_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad


            hrc_cookie.get_hotel_cookie(target='KIH')
            hrc_cookie.get_hotel_cookie(target='GSM')
            hrc_cookie.get_hotel_cookie(target='SYZ')
            hrc_cookie.get_hotel_cookie(target='MHD')
            hrc_cookie.get_hotel_cookie(target='THR')
            hrc_cookie.get_hotel_cookie(target='IFN')
            hrc_cookie.get_hotel_cookie(target='AZD')
            hrc_cookie.get_hotel_cookie(target='TBZ')



            hrc_cookie.get_hotel_cookie(target='AWZ')
            hrc_cookie.get_hotel_cookie(target='BND')
            hrc_cookie.get_hotel_cookie(target='ZBR')
            hrc_cookie.get_hotel_cookie(target='KER')
            hrc_cookie.get_hotel_cookie(target='KSH')
            hrc_cookie.get_hotel_cookie(target='RAS')
            hrc_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            hrc_cookie.insertCookie_intoDB(provider="hrc")


            # hrc_cookie.get_hotel_cookie()
            hrc_cookie.close_driver()
        elif sepehr_name == "omid_oj":


            # # ==== Retrieve from Redis ========
            # if (omid_oj_cookie.GetCookie_FromDB(provider="omid_oj")):
            #     return True


            omid_oj_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="omid_oj", company=company)


            omid_oj_cookie.get_tour_cookie(target="KIH")
            omid_oj_cookie.get_tour_cookie(target="GSM")
            omid_oj_cookie.get_tour_cookie(target="SYZ")
            omid_oj_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad


            omid_oj_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            omid_oj_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            omid_oj_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            omid_oj_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad

            omid_oj_cookie.get_hotel_cookie(target='KIH')
            omid_oj_cookie.get_hotel_cookie(target='GSM')
            omid_oj_cookie.get_hotel_cookie(target='SYZ')
            omid_oj_cookie.get_hotel_cookie(target='MHD')
            omid_oj_cookie.get_hotel_cookie(target='THR')
            omid_oj_cookie.get_hotel_cookie(target='IFN')
            omid_oj_cookie.get_hotel_cookie(target='AZD')
            omid_oj_cookie.get_hotel_cookie(target='TBZ')

            omid_oj_cookie.get_hotel_cookie(target='AWZ')
            omid_oj_cookie.get_hotel_cookie(target='BND')
            omid_oj_cookie.get_hotel_cookie(target='ZBR')
            omid_oj_cookie.get_hotel_cookie(target='KER')
            omid_oj_cookie.get_hotel_cookie(target='KSH')
            omid_oj_cookie.get_hotel_cookie(target='RAS')
            omid_oj_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            omid_oj_cookie.insertCookie_intoDB(provider="omid_oj")


            # omid_oj_cookie.get_hotel_cookie()
            omid_oj_cookie.close_driver()
        elif sepehr_name == "parmis":


            # # ==== Retrieve from Redis ========
            # if (parmis_cookie.GetCookie_FromDB(provider="parmis")):
            #     return True



            parmis_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="parmis", company=company)

            parmis_cookie.get_tour_cookie(target="KIH")
            parmis_cookie.get_tour_cookie(target="GSM")
            parmis_cookie.get_tour_cookie(target="SYZ")
            parmis_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            parmis_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            parmis_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            parmis_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            parmis_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            parmis_cookie.get_hotel_cookie(target='KIH')
            parmis_cookie.get_hotel_cookie(target='GSM')
            parmis_cookie.get_hotel_cookie(target='SYZ')
            parmis_cookie.get_hotel_cookie(target='MHD')
            parmis_cookie.get_hotel_cookie(target='THR')
            parmis_cookie.get_hotel_cookie(target='IFN')
            parmis_cookie.get_hotel_cookie(target='AZD')
            parmis_cookie.get_hotel_cookie(target='TBZ')


            parmis_cookie.get_hotel_cookie(target='AWZ')
            parmis_cookie.get_hotel_cookie(target='BND')
            parmis_cookie.get_hotel_cookie(target='ZBR')
            parmis_cookie.get_hotel_cookie(target='KER')
            parmis_cookie.get_hotel_cookie(target='KSH')
            parmis_cookie.get_hotel_cookie(target='RAS')
            parmis_cookie.get_hotel_cookie(target='SRY')

            # ---- insert into DB
            parmis_cookie.insertCookie_intoDB(provider="parmis")


            # parmis_cookie.get_hotel_cookie()
            parmis_cookie.close_driver()
        elif sepehr_name == "hamsafar":

            # # ==== Retrieve from Redis ========
            # if (hamsafar_cookie.GetCookie_FromDB(provider="hamsafar")):
            #     return True


            hamsafar_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="hamsafar", company=company)
            hamsafar_cookie.get_tour_cookie(target="KIH")
            hamsafar_cookie.get_tour_cookie(target="GSM")
            hamsafar_cookie.get_tour_cookie(target="SYZ")
            hamsafar_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            hamsafar_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            hamsafar_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            hamsafar_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            hamsafar_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            hamsafar_cookie.get_hotel_cookie(target='KIH')
            hamsafar_cookie.get_hotel_cookie(target='GSM')
            hamsafar_cookie.get_hotel_cookie(target='SYZ')
            hamsafar_cookie.get_hotel_cookie(target='MHD')
            hamsafar_cookie.get_hotel_cookie(target='THR')
            hamsafar_cookie.get_hotel_cookie(target='IFN')
            hamsafar_cookie.get_hotel_cookie(target='AZD')
            hamsafar_cookie.get_hotel_cookie(target='TBZ')

            hamsafar_cookie.get_hotel_cookie(target='AWZ')
            hamsafar_cookie.get_hotel_cookie(target='BND')
            hamsafar_cookie.get_hotel_cookie(target='ZBR')
            hamsafar_cookie.get_hotel_cookie(target='KER')
            hamsafar_cookie.get_hotel_cookie(target='KSH')
            hamsafar_cookie.get_hotel_cookie(target='RAS')
            hamsafar_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            hamsafar_cookie.insertCookie_intoDB(provider="hamsafar")

            # hamsafar_cookie.get_hotel_cookie()
            hamsafar_cookie.close_driver()
        elif sepehr_name == "iman_amin":

            # # ==== Retrieve from Redis ========
            # if (iman_cookie.GetCookie_FromDB(provider="iman_amin")):
            #     return True


            iman_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="iman_amin", company=company)

            iman_cookie.get_tour_cookie(target="KIH")
            iman_cookie.get_tour_cookie(target="GSM")
            iman_cookie.get_tour_cookie(target="SYZ")
            iman_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            iman_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            iman_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            iman_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            iman_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            iman_cookie.get_hotel_cookie(target='KIH')
            iman_cookie.get_hotel_cookie(target='GSM')
            iman_cookie.get_hotel_cookie(target='SYZ')
            iman_cookie.get_hotel_cookie(target='MHD')
            iman_cookie.get_hotel_cookie(target='THR')
            iman_cookie.get_hotel_cookie(target='IFN')
            iman_cookie.get_hotel_cookie(target='AZD')
            iman_cookie.get_hotel_cookie(target='TBZ')


            iman_cookie.get_hotel_cookie(target='AWZ')
            iman_cookie.get_hotel_cookie(target='BND')
            iman_cookie.get_hotel_cookie(target='ZBR')
            iman_cookie.get_hotel_cookie(target='KER')
            iman_cookie.get_hotel_cookie(target='KSH')
            iman_cookie.get_hotel_cookie(target='RAS')
            iman_cookie.get_hotel_cookie(target='SRY')

            # ---- insert into DB
            iman_cookie.insertCookie_intoDB(provider="iman_amin")

            # iman_cookie.get_hotel_cookie(target="GSM")
            iman_cookie.close_driver()
        elif sepehr_name == "flamingo":

            # # ==== Retrieve from Redis ========
            # if (flamingo_cookie.GetCookie_FromDB(provider="flamingo")):
            #     return True


            flamingo_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="flamingo", company=company)

            flamingo_cookie.get_tour_cookie(target="KIH")
            flamingo_cookie.get_tour_cookie(target="GSM")
            flamingo_cookie.get_tour_cookie(target="SYZ")
            flamingo_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            flamingo_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            flamingo_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            flamingo_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            flamingo_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad




            flamingo_cookie.get_hotel_cookie(target='KIH')
            flamingo_cookie.get_hotel_cookie(target='GSM')
            flamingo_cookie.get_hotel_cookie(target='SYZ')
            flamingo_cookie.get_hotel_cookie(target='MHD')
            flamingo_cookie.get_hotel_cookie(target='THR')
            flamingo_cookie.get_hotel_cookie(target='IFN')
            flamingo_cookie.get_hotel_cookie(target='AZD')
            flamingo_cookie.get_hotel_cookie(target='TBZ')

            flamingo_cookie.get_hotel_cookie(target='AWZ')
            flamingo_cookie.get_hotel_cookie(target='BND')
            flamingo_cookie.get_hotel_cookie(target='ZBR')
            flamingo_cookie.get_hotel_cookie(target='KER')
            flamingo_cookie.get_hotel_cookie(target='KSH')
            flamingo_cookie.get_hotel_cookie(target='RAS')
            flamingo_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            flamingo_cookie.insertCookie_intoDB(provider="flamingo")

            # flamingo_cookie.get_hotel_cookie(target="GSM")
            flamingo_cookie.close_driver()
        elif sepehr_name == 'shayan_gasht':

            # # ==== Retrieve from Redis ========
            # if (shayan_gasht_cookie.GetCookie_FromDB(provider="shayan_gasht")):
            #     return True


            shayan_gasht_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="shayan_gasht",
                                             company=company)

            shayan_gasht_cookie.get_tour_cookie(target="KIH")
            shayan_gasht_cookie.get_tour_cookie(target="GSM")
            shayan_gasht_cookie.get_tour_cookie(target="SYZ")
            shayan_gasht_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            shayan_gasht_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            shayan_gasht_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            shayan_gasht_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            shayan_gasht_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            shayan_gasht_cookie.get_hotel_cookie(target='KIH')
            shayan_gasht_cookie.get_hotel_cookie(target='GSM')
            shayan_gasht_cookie.get_hotel_cookie(target='SYZ')
            shayan_gasht_cookie.get_hotel_cookie(target='MHD')
            shayan_gasht_cookie.get_hotel_cookie(target='THR')
            shayan_gasht_cookie.get_hotel_cookie(target='IFN')
            shayan_gasht_cookie.get_hotel_cookie(target='AZD')
            shayan_gasht_cookie.get_hotel_cookie(target='TBZ')


            shayan_gasht_cookie.get_hotel_cookie(target='AWZ')
            shayan_gasht_cookie.get_hotel_cookie(target='BND')
            shayan_gasht_cookie.get_hotel_cookie(target='ZBR')
            shayan_gasht_cookie.get_hotel_cookie(target='KER')
            shayan_gasht_cookie.get_hotel_cookie(target='KSH')
            shayan_gasht_cookie.get_hotel_cookie(target='RAS')
            shayan_gasht_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            shayan_gasht_cookie.insertCookie_intoDB(provider="shayan_gasht")

            # shayan_gasht_cookie.get_hotel_cookie(target="GSM")
            shayan_gasht_cookie.close_driver()
        elif sepehr_name == 'dolfin':

            # # ==== Retrieve from Redis ========
            # if (dolfin_cookie.GetCookie_FromDB(provider="dolfin")):
            #     return True

            dolfin_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="dolfin", company=company)
            dolfin_cookie.get_tour_cookie(target="KIH")
            dolfin_cookie.get_tour_cookie(target="GSM")
            dolfin_cookie.get_tour_cookie(target="SYZ")
            dolfin_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            dolfin_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            dolfin_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            dolfin_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            dolfin_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            dolfin_cookie.get_hotel_cookie(target='KIH')
            dolfin_cookie.get_hotel_cookie(target='GSM')
            dolfin_cookie.get_hotel_cookie(target='SYZ')
            dolfin_cookie.get_hotel_cookie(target='MHD')
            dolfin_cookie.get_hotel_cookie(target='THR')
            dolfin_cookie.get_hotel_cookie(target='IFN')
            dolfin_cookie.get_hotel_cookie(target='AZD')
            dolfin_cookie.get_hotel_cookie(target='TBZ')


            dolfin_cookie.get_hotel_cookie(target='AWZ')
            dolfin_cookie.get_hotel_cookie(target='BND')
            dolfin_cookie.get_hotel_cookie(target='ZBR')
            dolfin_cookie.get_hotel_cookie(target='KER')
            dolfin_cookie.get_hotel_cookie(target='KSH')
            dolfin_cookie.get_hotel_cookie(target='RAS')
            dolfin_cookie.get_hotel_cookie(target='SRY')

            # ---- insert into DB
            dolfin_cookie.insertCookie_intoDB(provider="dolfin")


            # dolfin_cookie.get_hotel_cookie(target="GSM")
            dolfin_cookie.close_driver()
        elif sepehr_name == 'yegane_fard':

            # # ==== Retrieve from Redis ========
            # if (yegane_fard_cookie.GetCookie_FromDB(provider="yegane_fard")):
            #     return True


            yegane_fard_cookie.login_sepehr(recaptcha_value=recaptcha_code, provider_code="yegane_fard",
                                            company=company)

            yegane_fard_cookie.get_tour_cookie(target="KIH")
            yegane_fard_cookie.get_tour_cookie(target="GSM")
            yegane_fard_cookie.get_tour_cookie(target="SYZ")
            yegane_fard_cookie.get_tour_cookie(target="MHD", SourceMabda="THR")  # baraye ashhad

            yegane_fard_cookie.get_tour_cookie(target="THR", SourceMabda="MHD")  # baraye ashhad
            yegane_fard_cookie.get_tour_cookie(target="IFN", SourceMabda="THR")  # baraye ashhad
            yegane_fard_cookie.get_tour_cookie(target="AZD", SourceMabda="THR")  # baraye ashhad
            yegane_fard_cookie.get_tour_cookie(target="TBZ", SourceMabda="THR")  # baraye ashhad



            yegane_fard_cookie.get_hotel_cookie(target='KIH')
            yegane_fard_cookie.get_hotel_cookie(target='GSM')
            yegane_fard_cookie.get_hotel_cookie(target='SYZ')
            yegane_fard_cookie.get_hotel_cookie(target='MHD')
            yegane_fard_cookie.get_hotel_cookie(target='THR')
            yegane_fard_cookie.get_hotel_cookie(target='IFN')
            yegane_fard_cookie.get_hotel_cookie(target='AZD')
            yegane_fard_cookie.get_hotel_cookie(target='TBZ')

            yegane_fard_cookie.get_hotel_cookie(target='AWZ')
            yegane_fard_cookie.get_hotel_cookie(target='BND')
            yegane_fard_cookie.get_hotel_cookie(target='ZBR')
            yegane_fard_cookie.get_hotel_cookie(target='KER')
            yegane_fard_cookie.get_hotel_cookie(target='KSH')
            yegane_fard_cookie.get_hotel_cookie(target='RAS')
            yegane_fard_cookie.get_hotel_cookie(target='SRY')


            # ---- insert into DB
            yegane_fard_cookie.insertCookie_intoDB(provider="yegane_fard")


            # yegane_fard_cookie.get_hotel_cookie(target="GSM")
            yegane_fard_cookie.close_driver()
        else:
            return Response(
                {'message': "sepehr name is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # ---
        CookieProvider.objects.create(
            name=sepehr_name,
            recaptcha_code=recaptcha_code,
            company=company
        )
        return Response(
            {"message": "seated"},
            status=status.HTTP_200_OK
        )

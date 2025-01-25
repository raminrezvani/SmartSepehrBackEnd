from app_crawl.calendar.sepehr import SepehrCalendar
from app_crawl.calendar.mojalalsafar_crawler_Calendar import MojalalSafarCalendar

class CalendarData:
    def __init__(self, source, target, skip_month=0):
        self.source = source
        self.target = target
        self.skip_month = skip_month

    def get_result(self):
        sepehr = SepehrCalendar(source=self.source, target=self.target, skip_month=self.skip_month)
        sepehrResult=sepehr.get_result()
        #--- mojalal
        try:
            mojalal = MojalalSafarCalendar(source=self.source, target=self.target, skip_month=self.skip_month)
            mojalalResult=mojalal.get_result()
        except:
            mojalalResult={}
            mojalalResult['go']=[]
            mojalalResult['return']=[]

        #-- Integrate--
        integratedResult=sepehrResult



        final_result={
            'go':[],
            'return':[]
        }

        if (len(integratedResult['go'])==0):
            final_result['go']=mojalalResult['go']
        if (len(integratedResult['return']) == 0):
            final_result['return'] = mojalalResult['return']

        if (len(mojalalResult['go']) == 0):
            final_result['go'] = integratedResult['go']
        if (len(mojalalResult['return']) == 0):
            final_result['return'] = integratedResult['return']


        if (len(integratedResult['go'])!=0 and len(mojalalResult['go'])!=0):
            for item, item2 in zip(integratedResult['go'], mojalalResult['go']):
                if item['date'] == item2['date'] and int(item['price']) > int(item2['price']):
                    # print(f'Go_occurred === {item["date"]}')
                    item['price'] = item2['price']
            final_result['go']=integratedResult['go']

        if (len(integratedResult['return']) != 0 and len(mojalalResult['return']) != 0):
            for item, item2 in zip(integratedResult['return'], mojalalResult['return']):
                if item['date'] == item2['date'] and int(item['price']) > int(item2['price']):
                    # print(f'return_occurred === {item["date"]}')
                    item['price'] = item2['price']

            final_result['return']=integratedResult['return']


        return final_result

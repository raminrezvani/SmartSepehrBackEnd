from app_crawl.calendar.sepehr import SepehrCalendar
from app_crawl.calendar.mojalalsafar_crawler_Calendar import MojalalSafarCalendar
from concurrent.futures import ThreadPoolExecutor

class CalendarData:
    def __init__(self, source, target, skip_month=0):
        self.source = source
        self.target = target
        self.skip_month = skip_month



    def get_result(self):

        with ThreadPoolExecutor() as executor:
            # Execute both tasks in parallel
            future_sepehr = executor.submit(SepehrCalendar, self.source, self.target, self.skip_month)
            future_mojalal = executor.submit(MojalalSafarCalendar, self.source, self.target, self.skip_month)

            # Get results
            sepehrResult = future_sepehr.result().get_result()

            try:
                mojalalResult = future_mojalal.result().get_result()
            except:
                mojalalResult = {"go": [], "return": []}

        # Initialize final result structure
        final_result = {
            "go": sepehrResult.get("go", []),
            "return": sepehrResult.get("return", [])
        }

        # Replace empty results with Mojalal if necessary
        final_result["go"] = final_result["go"] or mojalalResult["go"]
        final_result["return"] = final_result["return"] or mojalalResult["return"]

        # Merge price data efficiently
        if sepehrResult["go"] and mojalalResult["go"]:
            final_result["go"] = [
                {**s, "price": min(int(s["price"]), int(m["price"]))} if s["date"] == m["date"] else s
                for s, m in zip(sepehrResult["go"], mojalalResult["go"])
            ]

        if sepehrResult["return"] and mojalalResult["return"]:
            final_result["return"] = [
                {**s, "price": min(int(s["price"]), int(m["price"]))} if s["date"] == m["date"] else s
                for s, m in zip(sepehrResult["return"], mojalalResult["return"])
            ]

        return final_result


    def get_result_old(self):
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

#pip install uvicorn
#uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000 --workers 4


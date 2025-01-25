import after_response
from app_report.models import SearchReport


@after_response.enable
def add_search_report(data):
    try:
        SearchReport.objects.create(**data)
    except:
        print("--------------------------------------")
        print("something went wrong in add search report")

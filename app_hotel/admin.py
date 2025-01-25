from app_utils.main_model import MainModelAdmin, admin
from app_hotel.models import Hotel


@admin.register(Hotel)
class HotelAdmin(MainModelAdmin):
    list_display = ("name", "city_code", "detail_content")
    search_fields = ("name", "city_code")
    list_filter = ['city_code']

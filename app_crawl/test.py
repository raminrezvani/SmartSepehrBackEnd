import re

nm = "05هتل بهشت 3* (بازسازي شده فاز جديد )"


def ready_sepehr_gsm_hotel_name(name: str) -> str:
    """
    remove sepehr gsm hotel name noises
    :param name: hotel name
    :return: hotel name without noise
    """
    name = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", name)
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.replace('قشم', '')
    name = name.replace('درگهان', '')
    name = name.replace('ُ', '')  # ُ
    name = name.replace('ي', 'ی')
    name = name.replace('آ', 'ا')
    name = name.replace('قشم', '')
    name = name.replace('درگهان', '')
    name = name.replace('GSM', '')
    name = name.replace('gsm', '')
    name = name.replace('_', ' ')
    name = name.replace('  ', ' ')
    return name


name_2 = "بهشت"

print("--------------------------------")
print(ready_sepehr_gsm_hotel_name(nm), name_2, name_2 in ready_sepehr_gsm_hotel_name(nm))

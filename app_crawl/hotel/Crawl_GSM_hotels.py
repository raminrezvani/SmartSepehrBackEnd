import requests
# res=requests.get('https://www.eghamat24.com/QeshmHotels.html?gad_source=1&gclid=EAIaIQobChMI0erD79TEiAMV3p-DBx2tCzrrEAAYASAAEgK7wfD_BwE').text
with open('GheshmHotels.html','r',encoding='utf8') as fl:
    res=fl.read()

from lxml import etree
from io import StringIO
parser=etree.HTMLParser()
htmlparsed=etree.parse(StringIO(res),parser=parser)
lst_GSM_hotels=htmlparsed.xpath('//a[contains(@href,"/QeshmHotels/")]/@title')
fp=open('lst_GSM_hotels.txt','a',encoding='utf8')
for item in lst_GSM_hotels:
    fp.write(item+'\n')
fp.close()
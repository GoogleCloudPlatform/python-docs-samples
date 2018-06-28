import pprint
import json
import httplib2
import time

from googleapiclient.discovery import build

service = build('jobs', 'v2')

createCompanyRequest={'title':'Phoenix\'s Test Company', 'distributorCompanyId':'test_python_company_1231', 'hqLocation':'801 11th Ave, Sunnyvale, CA', 'companySize':'GIANT' }
response = service.companies().create(body=createCompanyRequest).execute()
companyName = response.get("name")
pprint.pprint("################") 
pprint.pprint(companyName)
pprint.pprint("################") 

updateCompanyRequest={'title':'Phoenix\'s Test Company 1', 'distributorCompanyId':'test_python_company_1', 'hqLocation':'801 11th Ave, Sunnyvale, CA', 'companySize':'GIANT' }
response = service.companies().patch(name=companyName, body=createCompanyRequest).execute()
pprint.pprint("######update response#####") 
pprint.pprint(response)
pprint.pprint("################") 

time.sleep(20)
service.companies().delete(name=companyName).execute()
pprint.pprint("#####Removed####") 
pprint.pprint(companyName)
pprint.pprint("################") 
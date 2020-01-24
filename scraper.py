import requests #import your libraries. This could be import requests as req  and then the following lines could be req.session()
import json
from pprint import pprint #we're importing the pprint function from pprint
import psycopg2


requests.packages.urllib3.disable_warnings() #urllib3 is a package required for requests so you don't need to install it yourself


headers = {
	"Host": "www.edmunds.com",
	"Connection": "keep-alive",
	"Accept": "application/json, text/javascript, */*; q=0.01",
	"X-Requested-With": "XMLHttpRequest",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
	"DNT": "1",
	"Referer": "https://www.edmunds.com/mazda/mx-5-miata/2008/",
	"Accept-Encoding": "gzip, deflate, sdch, br",
	"Accept-Language": "en-US,en;q=0.8",
	"Cookie": """i10c.sid=1484425743390; edw=702929808519982720; visid_incap_851464=E5fX21eDTL+bpsFtOev2a7WJelgAAAAAQUIPAAAAAAASdNr+AU3TdHVZtlA5fTkO; incap_ses_210_851464=uwKoFMuhq1344cIhsBLqArWJelgAAAAAMqyyEd/tmjT/bO8E3WiqMw==; m0r9h.salt=MOREPHEUS2$; i10c.SIBC=1; edmunds=e15dda40-da97-11e6-b16d-0242ac110002; JSESSIONID=49060B554B7F370FE5A7B3F90027989F; EdmundsYear="&zip=78703&dma=635:IP&city=Austin&state=TX&lat=&lon="; incap_ses_518_851464=7gflbeDm7xCgBvHAX04wB7aJelgAAAAA+pJIO63bTSKUOBlOP2jPlw==; content-targeting=US,TX,Austin,0,-97.7663,30.2966,78703; device-characterization=false,false""" #we are using the triple parentheses because there are parentheses in the cookie that were messing the syntax up
}

session = requests.session() #make a requests session, you can do stuff like request.get, request.post, etc... 
#but if we have cookies and such this session will store it and keep track of it as well as security tokens, etc...
#you can if you want set your headers and cookies to customize your requests
#session is a class within requests

response = session.get("https://www.edmunds.com/g00/2_d3d3LmVkbXVuZHMuY29t_/TU9SRVBIRVVTMiRodHRwczovL3d3dy5lZG11bmRzLmNvbS9hcGkvdmVoaWNsZS92Mi9zdHlsZXMvMTAwOTMzOTY0P3ZpZXc9ZnVsbCZpMTBjLm1hcmsueGhyLnR5cGU%3D_$/$/$/$/$/$",verify=False,allow_redirects=True,headers=headers) #take off the http and after on this line from the url, won't work otherwise
#try get: GET https://www.edmunds.com/api/vehicle/v3/submodels?makeNiceId=acura&fields=id%2Cname%2CniceId%2CmakeName%2CmakeNiceName%2CmodelName%2CmodelNiceId%2Cyear%2CpublicationStates&sortby=name&publicationStates=NEW%2CNEW_USED%2CPRE_PROD%2CUSED&pagenum=1&pagesize=1500 HTTP/1.1
#you can lookup the request library on google and find why you need these certain parameters
#verify = false is saying ignore SSL verification, were it true it would use SSL and that would make things more complicated

data = json.loads(response.text) #takes the text from the get response (the body)

pprint(data)
print(data.keys())
print(data["transmission"]["automaticType"])

_db = "car_info"
_user = "postgres"
_password = "#######"
_pgconnection = psycopg2.connect("dbname=%s user=%s password=%s"%(_db, _user, _password))
def execute(sql, params = None):
    cursor = _pgconnection.cursor()
    try:
        cursor.execute(sql, params)
    except Exception as e:
        print(e.pgerror)
        print(sql, params)
        # _pgconnection.rollback()
        raise
    _pgconnection.commit()
    cursor.close()

def execute_with_results(sql, params = None):
    cursor = _pgconnection.cursor()
    try:
        cursor.execute(sql, params)
    except Exception as e:
        print(e.pgerror)
        print(sql, params)
        # _pgconnection.rollback()
        raise
    if (cursor.rowcount <= 0):
        results = None
    else:
        results = cursor.fetchall()
    columns = [desc for desc in cursor.description]
    _pgconnection.commit()
    cursor.close()
    return results, columns

execute("insert into names (name) values (%s)",[json.dumps(data)])

import requests
import xmltodict
import json
import pprint
import re
from config import FUSEKI_PASSWORD


url = "https://portal.odissei.nl/sitemap.xml"
fusekiurl = "https://fuseki.odissei.nl"
user = 'admin'
password = FUSEKI_PASSWORD
response = requests.get(url)
collection = 'odissei'
doc = xmltodict.parse(response.text)
pp = pprint.PrettyPrinter(indent=4)


def uploadRDF(lasturl):
    response = requests.get(lasturl)
    print(json.loads(response.text))
    uploadfusekiurl = "%s/%s/data" % (fusekiurl, collection)
    resp = requests.post(uploadfusekiurl, data=response.text,
                         auth=(user, password),
                         headers={"Content-Type": "application/ld+json"})
    print(resp.text)
    return


for item in doc['urlset']['url']:
    hostitems = re.search("^(\S+)\/dataset\S+\?(persistent\S+)$", item['loc'])
    if hostitems:
        dvnurl = "%s/api/datasets/export?exporter=OAI_ORE&%s" % (
        hostitems.group(1), hostitems.group(2))
        print(dvnurl)
        try:
            uploadRDF(dvnurl)
        except:
            print("Ignore %s" % dvnurl)

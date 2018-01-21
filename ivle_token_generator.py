# -*- coding: utf-8 -*-
import requests
import logging

logger = logging.getLogger(__name__)

# Consider changing this to OOP style, but no benefit as of now

#==============================================================================
#                      Gets auth token from IVLE
#
#==============================================================================

## Main method.
def get_token(API_KEY,IVLE_LOGIN,IVLE_PASS,headers):
    viewstate = get_and_strip_viewstate(API_KEY,IVLE_LOGIN,IVLE_PASS,headers)
    URL = 'https://ivle.nus.edu.sg/api/login/?apikey='+API_KEY
    payload = {
        'userid': IVLE_LOGIN,
        'password': IVLE_PASS,
        '__VIEWSTATE':viewstate
    }
    with requests.Session() as s:
        x = s.get(URL, params=payload,headers=headers)
        token = x.text
        if validate_token(API_KEY,token,headers):
            return token
    logger.error("No token from LAPI received! Are your username and password correct?")
    return

#ASP.net uses viewstates for legit logins. just get it via python instead ;)
def get_and_strip_viewstate(API_KEY,IVLE_LOGIN,IVLE_PASS,headers):
    xml = getXML(API_KEY,IVLE_LOGIN,IVLE_PASS,headers)
    token = strip_token(xml)
    return token

def getXML(API_KEY,IVLE_LOGIN,IVLE_PASS,headers):
    URL = 'https://ivle.nus.edu.sg/api/login/?apikey=' + API_KEY +'&url=localhost'
    x = requests.get(URL,auth = (IVLE_LOGIN,IVLE_PASS),headers=headers)
    x = x.content.decode()
    return x

def strip_token(xml):
    word_to_find = 'value="/'
    startIdx = xml.find(word_to_find)
    token_half = xml[startIdx+len(word_to_find) - 1:]
    endIdx = token_half.find('"')
    token = token_half[:endIdx]
    return token

def validate_token(API_KEY,TOKEN,headers):
    URL = 'https://ivle.nus.edu.sg/api/Lapi.svc/Validate?APIKey='+API_KEY+'&Token='+TOKEN
    x = requests.get(URL,headers=headers).json()
    return True if x['Success'] == True else False
# -*- coding: utf-8 -*-
import requests

# Consider changing this to OOP style, but no benefit as of now

#==============================================================================
#                      Gets auth token from IVLE
# 
#==============================================================================

## Main method.    
def getToken(API_KEY,IVLE_LOGIN,IVLE_PASS,headers):
    viewstate = getAndStripViewstate(API_KEY,IVLE_LOGIN,IVLE_PASS,headers)
    URL = 'https://ivle.nus.edu.sg/api/login/?apikey='+API_KEY
    payload = {
        'userid': IVLE_LOGIN,
        'password': IVLE_PASS,
        '__VIEWSTATE':viewstate
    }
    with requests.Session() as s:
        x = s.get(URL, params=payload,headers=headers)
        token = x.text
        if validateToken(API_KEY,token,headers):
            return token
    return

#ASP.net uses viewstates for legit logins. just get it via python instead ;)
def getAndStripViewstate(API_KEY,IVLE_LOGIN,IVLE_PASS,headers):
    xml = getXML(API_KEY,IVLE_LOGIN,IVLE_PASS,headers)
    token = stripToken(xml)
    return token
    
def getXML(API_KEY,IVLE_LOGIN,IVLE_PASS,headers):
    URL = 'https://ivle.nus.edu.sg/api/login/?apikey=' + API_KEY +'&url=localhost'
    x = requests.get(URL,auth = (IVLE_LOGIN,IVLE_PASS),headers=headers)
    x = x.content.decode()
    return x

def stripToken(xml):
    word_to_find = 'value="/'
    startIdx = xml.find(word_to_find)
    token_half = xml[startIdx+len(word_to_find) - 1:]
    endIdx = token_half.find('"')
    token = token_half[:endIdx]
    return token
    
def validateToken(API_KEY,TOKEN,headers):
    URL = 'https://ivle.nus.edu.sg/api/Lapi.svc/Validate?APIKey='+API_KEY+'&Token='+TOKEN
    x = requests.get(URL,headers=headers).json()
    return True if x['Success'] == True else False
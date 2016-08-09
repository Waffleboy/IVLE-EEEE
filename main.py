# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 01:27:13 2016

@author: waffleboy
"""

import requests,os
# Token
import ivle_token_generator
# downloader from workbins
import workbin_files_downloader

FOLDER_DOWNLOAD_LOCATION = '/storage/NUS STUFF/LectureTutorials/IVLE'
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
API_KEY = os.environ['IVLE_LAPI_KEY']
IVLE_LOGIN = 'a0130737'
IVLE_PASS = os.environ['IVLE_PASS']
TOKEN = ivle_token_generator.getToken(API_KEY,IVLE_LOGIN,IVLE_PASS,headers)
filesDownloaded = {}

# get all mods taken in current semester
def getCurrSemMods():
    global API_KEY,TOKEN,headers
    URL = 'https://ivle.nus.edu.sg/api/Lapi.svc/Modules_Student?APIKey='+API_KEY+'&AuthToken='+TOKEN+'&Duration=0&IncludeAllInfo=true'
    modules = requests.get(URL,headers=headers).json()['Results']
    return modules

# get workbin ID from modules in current semester
def getWorkbinIDFromOpenMods(modules):
    dic = {}
    for module in modules:
        if module['Workbins']:
            dic[module['CourseCode']] = module['Workbins'][0]['ID']
    return dic

# get full workbins from workbin ID
def getAllWorkbinsFromWorkbinID(workbinID_dic):
    global API_KEY,TOKEN,headers
    workbins = []
    for WORKBIN_ID in workbinID_dic.values():
        URL='https://ivle.nus.edu.sg/api/Lapi.svc/Workbins?APIKey='+API_KEY+'&AuthToken='+TOKEN+'&WorkbinID='+WORKBIN_ID+'+&Duration=0'#&&TitleOnly=false'
        workbins.append(requests.get(URL,headers=headers).json()['Results'])
    return workbins
    
# print all files downloaded
def showFilesDownloaded():
    global filesDownloaded
    counter = 1
    print('%s New File(s) Downloaded' % len(filesDownloaded))
    for module in filesDownloaded:
        print('---- ' + module +' ----')
        for file in filesDownloaded[module]:
            print('%s. %s' % (counter,file))
            counter += 1
        counter = 1
    return
    

def run():
    global FOLDER_DOWNLOAD_LOCATION
    workbin_files_downloader.makeIfDoesntExist(FOLDER_DOWNLOAD_LOCATION)
    modules = getCurrSemMods()
    workbinIDs = getWorkbinIDFromOpenMods(modules)
    workbins = getAllWorkbinsFromWorkbinID(workbinIDs)
    workbin_files_downloader.downloadAll(workbins,workbinIDs,FOLDER_DOWNLOAD_LOCATION)
    showFilesDownloaded()
    
if __name__ == '__main__':
    run()
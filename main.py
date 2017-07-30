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

#==============================================================================
#                               Options
#==============================================================================
FOLDER_DOWNLOAD_LOCATION = '/storage/NUS_STUFF/LectureTutorials/IVLE'
API_KEY = os.environ['IVLE_LAPI_KEY']
IVLE_LOGIN = 'a0130737'
IVLE_PASS = os.environ['IVLE_PASS']
IGNORE_LIST = set(["OSA1003"])
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
TOKEN = ivle_token_generator.get_token(API_KEY,IVLE_LOGIN,IVLE_PASS,headers)
#==============================================================================

# get all mods taken in current semester
def get_curr_sem_mods():
    global API_KEY,TOKEN,headers
    URL = 'https://ivle.nus.edu.sg/api/Lapi.svc/Modules_Student?APIKey='+API_KEY+'&AuthToken='+TOKEN+'&Duration=0&IncludeAllInfo=true'
    modules = requests.get(URL,headers=headers).json()['Results']
    return modules

# get workbin ID from modules in current semester
def get_workbin_id_from_open_mods(modules):
    global IGNORE_LIST
    dic = {}
    for module in modules:
        if module['Workbins']:
            if module['CourseCode'] in IGNORE_LIST:
                continue
            dic[module['CourseCode']] = module['Workbins'][0]['ID']
    return dic

# get full workbins from workbin ID
def get_all_workbins_from_workbin_id(workbinID_dic):
    global API_KEY,TOKEN,headers
    workbins = []
    for WORKBIN_ID in workbinID_dic.values():
        URL='https://ivle.nus.edu.sg/api/Lapi.svc/Workbins?APIKey='+API_KEY+'&AuthToken='+TOKEN+'&WorkbinID='+WORKBIN_ID+'+&Duration=0'#&&TitleOnly=false'
        workbins.append(requests.get(URL,headers=headers).json()['Results'])
    return workbins
    

def run():
    global FOLDER_DOWNLOAD_LOCATION
    modules = get_curr_sem_mods()
    workbinIDs = get_workbin_id_from_open_mods(modules)
    workbins = get_all_workbins_from_workbin_id(workbinIDs)
    workbin_downloader = workbin_files_downloader.WorkbinFileDownloader(workbins,workbinIDs,FOLDER_DOWNLOAD_LOCATION,API_KEY,TOKEN)
    workbin_downloader.makeIfDoesntExist(FOLDER_DOWNLOAD_LOCATION) #from workbin downloader
    workbin_downloader.downloadAll() #from workbin downloader
    workbin_downloader.showFilesDownloaded()
    
if __name__ == '__main__':
    run()
# -*- coding: utf-8 -*-
import os,wgetter
#==============================================================================
# 
# This is in charge of downloading all files from the specified workbins.
# 
# Might want to change it to OOP in the future, but see no benefit as of yet.
# 
#==============================================================================


## Main function
# Input: < List > workbins:  List of workbins returned by IVLE
# Input: < Dic > workbinID_dic: Dictionary of ID : Name of workbin
# Input: < String> FOLDER_DOWNLOAD_LOCATION: file path of main folder to download to
def downloadAll(workbins,workbinID_dic,FOLDER_DOWNLOAD_LOCATION):
    reversed_workbin_id = reverseWorkbinID(workbinID_dic)
    for workbin in workbins:
        actual_workbin = workbin[0] # might crash in future - unknown if multiple workbins, files + folders etc.
        try:
            folders_in_workbin = actual_workbin['Folders']
        except:
            print('No folders for workbin: '+actual_workbin['Title'])
            continue
        module_code = reversed_workbin_id[actual_workbin['ID']]
        module_folder_path = FOLDER_DOWNLOAD_LOCATION+'/'+module_code
        makeIfDoesntExist(module_folder_path)
        for folder in folders_in_workbin:
            folder_path = module_folder_path + '/' + folder['FolderName']
            recursiveDownload(folder,folder_path)
    return

# Get workbin : ID instead
def reverseWorkbinID(workbinIDs):
    return {k:v for v,k in workbinIDs.items()}
    
# recursively download folders and files in subfolders
def recursiveDownload(folder,folder_path):
    makeIfDoesntExist(folder_path)
    otherFolders = folder['Folders']
    if otherFolders:
        for subfolder in otherFolders:
            subfolderPath = folder_path + '/' + subfolder['FolderName']
            recursiveDownload(subfolder,subfolderPath)
    downloadFilesIfDoesntExist(folder,folder_path)
    

##make folder if it doesnt exist.
def makeIfDoesntExist(folderDirectory):
    if not os.path.exists(folderDirectory):
        os.makedirs(folderDirectory)
    return

def downloadFilesIfDoesntExist(folder,folder_path):
    for file in folder['Files']:
        fileName = file['FileName']
        filePath = folder_path + '/' + fileName
        fileID = file['ID']
        downloadFileIfDoesntExist(fileName,fileID,filePath,folder_path)

def downloadFileIfDoesntExist(fileName,fileID,filePath,folder_path):
    if not os.path.exists(filePath):
        addToFilesDownloaded(fileName,folder_path)
        downloadFile(fileID,folder_path)
    return

def addToFilesDownloaded(fileName,folder_path):
    global filesDownloaded
    modCode = getModuleCodeFromFolderPath(folder_path)
    if modCode in filesDownloaded:
        filesDownloaded[modCode].append(fileName)
    else:
        filesDownloaded[modCode] = [fileName]
    return

def downloadFile(fileID,folder_path):
    global API_KEY,TOKEN
    URL = 'https://ivle.nus.edu.sg/api/downloadfile.ashx?APIKey='+API_KEY+'&AuthToken='+TOKEN+'&ID='+fileID+'&target=workbin'
    wgetter.download(URL,outdir=folder_path)
    return
    
def getModuleCodeFromFolderPath(string):
    global FOLDER_DOWNLOAD_LOCATION
    skip = len(FOLDER_DOWNLOAD_LOCATION) + 1
    startIdx = string.find(FOLDER_DOWNLOAD_LOCATION) + skip
    s = string[startIdx:]
    return s[:s.find('/')]
    

# -*- coding: utf-8 -*-
import os,wgetter
#==============================================================================
# 
# This is in charge of downloading all files from the specified workbins.
# 
#==============================================================================


class WorkbinFileDownloader():

    def __init__(self,workbins,workbinID_dic,FOLDER_DOWNLOAD_LOCATION,API_KEY,TOKEN):
        self.workbins = workbins
        self.workbinID_dic = workbinID_dic
        self.FOLDER_DOWNLOAD_LOCATION = FOLDER_DOWNLOAD_LOCATION
        self.API_KEY = API_KEY
        self.TOKEN = TOKEN
        self.filesDownloaded = {}

    ## Main function - downloads all files in the workbins given.
    def downloadAll(self):
        reversed_workbin_id = self.reverseWorkbinID(self.workbinID_dic)
        for workbin in self.workbins:
            actual_workbin = workbin[0] # might crash in future - unknown if multiple workbins, files + folders etc.
            try:
                folders_in_workbin = actual_workbin['Folders']
            except:
                print('No folders for workbin: '+actual_workbin['Title'])
                continue
            module_code = reversed_workbin_id[actual_workbin['ID']]
            module_folder_path = self.FOLDER_DOWNLOAD_LOCATION+'/'+module_code
            self.makeIfDoesntExist(module_folder_path)
            for folder in folders_in_workbin:
                folder_path = module_folder_path + '/' + folder['FolderName']
                self.recursiveDownload(folder,folder_path)
        return
    
    # Get workbin : ID instead
    def reverseWorkbinID(self,workbinIDs):
        return {k:v for v,k in workbinIDs.items()}
        
    # recursively download folders and files in subfolders
    def recursiveDownload(self,folder,folder_path):
        self.makeIfDoesntExist(folder_path)
        otherFolders = folder['Folders']
        if otherFolders:
            for subfolder in otherFolders:
                subfolderPath = folder_path + '/' + subfolder['FolderName']
                self.recursiveDownload(subfolder,subfolderPath)
        self.downloadFilesIfDoesntExist(folder,folder_path)
        
    
    ##make folder if it doesnt exist.
    def makeIfDoesntExist(self,folderDirectory):
        if not os.path.exists(folderDirectory):
            os.makedirs(folderDirectory)
        return
    
    def downloadFilesIfDoesntExist(self,folder,folder_path):
        for file in folder['Files']:
            fileName = file['FileName']
            filePath = folder_path + '/' + fileName
            fileID = file['ID']
            self.downloadFileIfDoesntExist(fileName,fileID,filePath,folder_path)
    
    def downloadFileIfDoesntExist(self,fileName,fileID,filePath,folder_path):
        if not os.path.exists(filePath):
            self.addToFilesDownloaded(fileName,folder_path)
            self.downloadFile(fileID,folder_path)
        return
    
    def addToFilesDownloaded(self,fileName,folder_path):
        global filesDownloaded
        modCode = self.getModuleCodeFromFolderPath(folder_path)
        if modCode in self.filesDownloaded:
            self.filesDownloaded[modCode].append(fileName)
        else:
            self.filesDownloaded[modCode] = [fileName]
        return
    
    def downloadFile(self,fileID,folder_path):
        URL = 'https://ivle.nus.edu.sg/api/downloadfile.ashx?APIKey='+self.API_KEY+'&AuthToken='+self.TOKEN+'&ID='+fileID+'&target=workbin'
        wgetter.download(URL,outdir=folder_path)
        return
        
    def getModuleCodeFromFolderPath(self,string):
        skip = len(self.FOLDER_DOWNLOAD_LOCATION) + 1
        startIdx = string.find(self.FOLDER_DOWNLOAD_LOCATION) + skip
        s = string[startIdx:]
        return s[:s.find('/')]
        
    # print all files downloaded
    def showFilesDownloaded(self):
        counter = 1
        totalFilesDownloaded = sum([len(x) for x in self.filesDownloaded.values()])
        print('%s New File(s) Downloaded' % totalFilesDownloaded)
        for module in self.filesDownloaded:
            print('---- ' + module +' ----')
            for file in self.filesDownloaded[module]:
                print('%s. %s' % (counter,file))
                counter += 1
            counter = 1
        return
    
    

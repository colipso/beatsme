#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 15:58:19 2017

@author: hp
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import re
import codecs

corpusDir = os.getcwd() + '/corpus'

class CreateDict:
    def __init__(self , folder = corpusDir):
        self.folder = folder
    def scanFile(self):
        '''
        
        '''
        result = {}
        for root,subdir,files  in os.walk(self.folder):
            if files != []:
                for oneFile in files:
                    print oneFile
                    f = codecs.open(root + '/' + oneFile , 'r','utf-8')
                    for line in f.readlines():
                        words = line.strip().split('|')
                        for w in words:
                            thaiList = re.findall(ur"[\u0E00-\u0E7F\.]+", w)
                            if thaiList != []:
                                s = u''
                                for t in thaiList:
                                    s += t
                                result.setdefault(s , 0)
                                result[s] += 1
                    f.close()
        return result
        
    def saveDict(self , data , fileName = 'dict.txt'):
        '''
        Parameter:
            data : {word : count , word2: count2}
        '''
        f = codecs.open(os.getcwd() + '/' + fileName , 'w' , 'utf-8')
        for (word,value) in sorted(data.items() , key = lambda d:d[1] , reverse = True):
            string = word + ' '+ str(value) + '\n'
            f.write(string)
        f.close()
    
CD = CreateDict()
data = CD.scanFile()
CD.saveDict(data)
        
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 19:17:14 2017

@author: hp
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import codecs
import re
import math
from charset import charsets


dictFile = os.getcwd() + '/dict.txt'
emitProbF = os.getcwd() + '/BMSE/emitProb.py'
startProbF = os.getcwd() + '/BMSE/startProb.py'
transProbF = os.getcwd() + '/BMSE/transProb.py'

corpusDir = os.getcwd() + '/corpus'

infinite = -3.14e+100

class StaticBMSE:
    def __init__(self , dictFile = dictFile):
        self.dicF = dictFile
        self.dic = {}
    def readDict(self):
        '''
        read corpus dict. word , wordcount
        '''
        f = codecs.open(self.dicF , 'r' , 'utf-8')
        for line in f.readlines():
            data = line.strip().strip('\n').split()
            if len(data) == 2:
                self.dic.setdefault(data[0] , int(data[1]))
        f.close()
            
    def staticEmissionProb(self):
        '''
        static emission probability.B is begin.E is END . M is middle of a word.
        S means a char is a single word.
        '''
        if self.dic == {}:
            self.readDict()
        allWordCount = sum(self.dic.values())
        self.emissionProb = {}
        emissionCount = {}
        emissionCount.setdefault('B' , {})
        emissionCount.setdefault('M' , {})
        emissionCount.setdefault('S' , {})
        emissionCount.setdefault('E' , {})
        for word in self.dic:
            if len(word) == 1:
                emissionCount['S'].setdefault(word , 0)
                emissionCount['S'][word] += self.dic[word]
            else:
                for x in range(len(word)):
                    if x == 0:
                        emissionCount['B'].setdefault(word[x] , 0)
                        emissionCount['B'][word[x]] += self.dic[word]
                    elif x == len(word)-1:
                        emissionCount['E'].setdefault(word[x] , 0)
                        emissionCount['E'][word[x]] += self.dic[word]
                    else:
                        emissionCount['M'].setdefault(word[x] , 0)
                        emissionCount['M'][word[x]] += self.dic[word]
        for key in emissionCount.keys():
            self.emissionProb.setdefault(key , {})
            for w in emissionCount[key]:
                self.emissionProb[key].setdefault(w , math.log(emissionCount[key][w]*1.0/allWordCount))
        
        
        for key in self.emissionProb:
            for oneChar in charsets:
                if oneChar not in self.emissionProb[key].keys():
                    self.emissionProb[key][oneChar] = infinite
        return True
    
    def saveEmissionProb(self , emitF = emitProbF):
        '''
        Save emission prob as a python file. Which can load directly
        '''       
        stringB = ''
        stringM = ''
        stringS = ''
        stringE = ''
        
        for word in self.emissionProb['B']:
            stringB += "u'%s':%s,\n" % (word,str(self.emissionProb['B'][word]))
        
        for word in self.emissionProb['M']:
            stringM += "u'%s':%s,\n" % (word,str(self.emissionProb['M'][word]))
            
        for word in self.emissionProb['S']:
            stringS += "u'%s':%s,\n" % (word,str(self.emissionProb['S'][word]))
        
        for word in self.emissionProb['E']:
            stringE += "u'%s':%s,\n" % (word,str(self.emissionProb['E'][word]))
        
        f = codecs.open(emitF , 'w' , 'utf-8')
        f.write('# -*- coding: utf-8 -*-\n')
        f.write("P={'B': {%s},'M':{%s},'S':{%s},'E':{%s}}" % (stringB , stringM ,stringS , stringE))
        f.close()
        return True
                

    def staticStartProb(self):
        '''
        '''
        if self.dic == {}:
            self.readDict()
        startProbCount = {}
        startProbCount.setdefault('B' , 0)
        startProbCount.setdefault('S' , 0)
        allWordCount = sum(self.dic.values())
        for word in self.dic:
            if len(word) == 1:
                startProbCount['S'] += 1
            else:
                startProbCount['B'] += 1
        self.startProb = {}
        self.startProb.setdefault('E' , infinite)
        self.startProb.setdefault('M' , infinite)
        
        self.startProb.setdefault('S' , math.log(startProbCount['S']*1.0 / allWordCount))
        self.startProb.setdefault('B' , math.log(startProbCount['B']*1.0 / allWordCount))
        return True
    
    def saveStartProb(self , startF = startProbF):
        '''
        '''
        f = codecs.open(startF , 'w' , 'utf-8')
        f.write('# -*- coding: utf-8 -*-\n')
        f.write("P={'B': %s,\n'M':%s,\n'S':%s,\n'E':%s}" % 
                (str(self.startProb['B']) , str(self.startProb['M']) ,str(self.startProb['S']) , str(self.startProb['E'])))
        f.close()
        return True
        
    
    def staticTransProb(self):
        '''
        '''
        resultCount = {'B': {'E': 0, 'M': 0},
                 'E': {'B': 0, 'S': 0},
                 'M': {'E': 0, 'M': 0},
                 'S': {'B': 0, 'S': 0}}
        
        for root,subdir,files in os.walk(corpusDir):
            #print root , subdir , files
            if files != []:
                for oneFile in files:
                    f = codecs.open(root + '/' + oneFile , 'r','utf-8')
                    for line in f.readlines():
                        words = line.strip().split('|')
                        oneList = []
                        for w in words:
                            thaiList = re.findall(ur"[\u0E00-\u0E7F\.]+", w)
                            if thaiList != []:
                                s = u''
                                for t in thaiList:
                                    s += t
                            oneList.append(s)
                        if len(oneList) > 1:
                            #wordCount += len(oneList)
                            for i in range(len(oneList)-1):
                                if len(oneList[i]) == 1:       #single
                                    if len(oneList[i+1]) == 1:
                                        resultCount['S']['S'] += 1
                                    if len(oneList[i+1]) > 1:
                                        resultCount['S']['B'] += 1
                                if len(oneList[i]) == 2:
                                    resultCount['B']['E'] += 1
                                    if len(oneList[i+1]) == 1:
                                        resultCount['E']['S'] += 1
                                    if len(oneList[i+1]) > 1:
                                        resultCount['E']['B'] += 1
                                if len(oneList[i]) > 2:
                                    resultCount['B']['M'] += len(oneList[i])-2
                                    resultCount['M']['E'] += 1
                                    resultCount['M']['M'] += len(oneList[i])-3
                                    if len(oneList[i+1]) == 1:
                                        resultCount['E']['S'] += 1
                                    if len(oneList[i+1]) > 1:
                                        resultCount['E']['B'] += 1
                            if len(oneList[-1]) == 1:
                                resultCount['S']['B'] += 1 #suppose the first word of next line is not a one character word 
                            elif len(oneList[-1]) == 2:
                                resultCount['B']['E'] += 1
                                resultCount['E']['B'] += 1
                            elif len(oneList[-1]) > 2:
                                resultCount['B']['M'] += 1
                                resultCount['M']['E'] += 1
                                resultCount['M']['M'] += len(oneList[-1])-3
                                resultCount['E']['B'] += 1
                    f.close()
        charCount = 0
        for key in resultCount:
            for secKey in resultCount[key]:
                charCount += resultCount[key][secKey]
        self.transProb = {}
        for key in resultCount:
            self.transProb.setdefault(key , {})
            for secKey in resultCount[key]:
                self.transProb[key].setdefault( secKey , math.log(resultCount[key][secKey] * 1.0 / charCount))
                
        #print resultCount , wordCount  ,self.transProb
        return True
    def saveTransProb(self , transF = transProbF):
        '''
        '''
        f = codecs.open(transF , 'w' , 'utf-8')
        f.write('# -*- coding: utf-8 -*-\n')
        f.write("P={'B': {'E': %s, 'M': %s},\n'E': {'B': %s, 'S': %s},\n'M': {'E': %s, 'M': %s},\n'S': {'B': %s, 'S': %s}}" % 
                (
                str(self.transProb['B']['E']) , str(self.transProb['B']['M']) ,
                str(self.transProb['E']['B']) , str(self.transProb['E']['S']),
                str(self.transProb['M']['E']) , str(self.transProb['M']['M']),
                str(self.transProb['S']['B']) , str(self.transProb['S']['S'])
                )
            )
        f.close()
        return True
    
    def run(self):
        self.staticEmissionProb()
        self.saveEmissionProb()
        self.staticStartProb()
        self.saveStartProb()
        self.staticTransProb()
        self.saveTransProb()
        
            
            
            

StaticBMSE().run()
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 19:22:45 2017

@author: hp
"""

import os
import math
from BMSE import *
start_Prob = startP
emit_Prob = emitP
trans_Prob = transP
states = ['B' , 'M' ,'S' ,'E']

import re
import sys

re_thai_default = re.compile("([\u0E00-\u0E7Fa-zA-Z0-9+#&\._]+)", re.U)
re_eng = re.compile('[a-zA-Z0-9]', re.U)

thisdir = os.path.split(os.path.realpath(__file__))[0]

dictf =  thisdir + '/dict.txt'


class HMM:
    def __init__(self , start_P = start_Prob , emit_P = emit_Prob , trans_P = trans_Prob , dictf = dictf):
        self.startP = start_P
        self.emitP = emit_P
        self.transP = trans_P
        
        lfreq = {}
        ltotal = 0
        f = open(dictf)
        #f_name = resolve_filename(f)
        for lineno, line in enumerate(f, 1):
            try:
                line = line.strip().decode('utf-8')
                word, freq = line.split(' ')[:2]
                freq = int(freq)
                lfreq[word] = freq
                ltotal += freq
                for ch in xrange(len(word)):
                    wfrag = word[:ch + 1]
                    if wfrag not in lfreq:
                        lfreq[wfrag] = 0
            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (dictf, lineno, line))
        f.close()
        self.FREQ = lfreq
        self.total = ltotal
        
    def pureCut(self ,sentence):
        '''
        Input:
            @centence : a string 
        '''
        viterbiP = [{}]
        path = {}
        #firt char probability
        for S in states:
            viterbiP[0][S] = self.startP[S] + self.emitP[S][sentence[0]]
            path[S] = [S]

        
        for t in range(1,len(sentence)):
            viterbiP.append({})
            newPath = {}
            for thisS in states:
                prob_lastState_list = []
                for lastS in states:
                    if lastS == 'B' and (thisS == 'B' or thisS == 'S'):
                        continue
                    elif lastS == 'M' and (thisS == 'B' or thisS == 'S'):
                        continue
                    elif lastS == 'S' and (thisS == 'M' or thisS == 'E'):
                        continue
                    elif lastS == 'E' and (thisS == 'M' or thisS == 'E'):
                        continue
                    prob_lastState_list.append( (viterbiP[t-1][lastS] + self.transP[lastS][thisS] + self.emitP[thisS][sentence[t]] , lastS)  )
                (prob , lastState) = max(prob_lastState_list)
                viterbiP[t][thisS] = prob
                newPath[thisS] = path[lastState] + [thisS]
            path = newPath
        (maxProb ,finalState) = max((viterbiP[ len(sentence) - 1 ] , S) for S in states)
        finalSequence = path[finalState]
        #debug
        print finalSequence
        #enddebug
        s =''
        for i in range(len(sentence)):
            if finalSequence[i] == 'S':
                yield sentence[i]
            elif finalSequence[i] == 'B':
                s += sentence[i]
            elif finalSequence[i] == 'M':
                s += sentence[i]
            elif finalSequence[i] == 'E':
                s += sentence[i]
                yield s
                s = ''
                
    
    def get_DAG(self , sentence):
    #self.check_initialized()
        DAG = {}
        N = len(sentence)
        for k in xrange(N):
            tmplist = []
            i = k
            frag = sentence[k]
            while i < N and frag in self.FREQ:
                if self.FREQ[frag]:
                    tmplist.append(i)
                i += 1
                frag = sentence[k:i + 1]
            if not tmplist:
                tmplist.append(k)
            DAG[k] = tmplist
        return DAG
    
    def calc(self ,sentence, DAG, route):
        N = len(sentence)
        route[N] = (0, 0)
        logtotal = math.log(self.total)
        for idx in xrange(N - 1, -1, -1):
            route[idx] = max((math.log(self.FREQ.get(sentence[idx:x + 1]) or 1) -
                              logtotal + route[x + 1][0], x) for x in DAG[idx])
            
    def cut_DAG_NO_HMM(self , sentence):
        DAG = self.get_DAG(sentence)
        route = {}
        self.calc(sentence, DAG, route)
        x = 0
        N = len(sentence)
        buf = ''
        while x < N:
            y = route[x][1] + 1
            l_word = sentence[x:y]
            if re_eng.match(l_word) and len(l_word) == 1:
                buf += l_word
                x = y
            else:
                if buf:
                    yield buf
                    buf = ''
                yield l_word
                x = y
        if buf:
            yield buf
            buf = ''

    def Cut(self,sentence):
        '''
        Input:
            @centence : a string 
        '''
        if sentence.strip() == '':
            yield ''
        for sentence_splitFirst in sentence.split():
            sentence_splited = re_thai_default.split(sentence_splitFirst)
            for sen in sentence_splited:
                #print sen
                if re_thai_default.match(sen):
                    for r in self.pureCut(sen):
                        yield r
                else:
                   yield sen   
                
                
#test
'''
#sentence:|เป็น|การ|ศึกษา|ที่ตั้ง|อยู่|บน|สมมุติฐาน|ที่|ไม่|ได้|มี|ลักษณะ|ที่|ดี|มาก|นัก| |ใน|สายตา|ของ|ผู้|ที่|นิยม|เรื่อง|ความ|เป็น|กลาง|ใน|การ|วิจัย| 
sentence = u'เป็นการศึกษาที่ตั้งอยู่บนสมมุติฐานที่ไม่ได้มีลักษณะที่ดีมากนักในสายตาของผู้ที่นิยมเรื่องความเป็นกลางในการวิจัย'
sentence = u'วิทยาลัยนาฏศิลปกาฬสินธุ์'
H = HMM()
result = H.cut_DAG_NO_HMM(sentence)
for r in result:
    print r
'''


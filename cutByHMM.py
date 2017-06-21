#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 19:22:45 2017

@author: hp
"""

import math
from BMSE import *
start_Prob = startP
emit_Prob = emitP
trans_Prob = transP
states = ['B' , 'M' ,'S' ,'E']


class HMM:
    def __init__(self , start_P = start_Prob , emit_P = emit_Prob , trans_P = trans_Prob):
        self.startP = start_P
        self.emitP = emit_P
        self.transP = trans_P

    def pureCut(self,sentence):
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
                
                
                
#test
#sentence:|เป็น|การ|ศึกษา|ที่ตั้ง|อยู่|บน|สมมุติฐาน|ที่|ไม่|ได้|มี|ลักษณะ|ที่|ดี|มาก|นัก| |ใน|สายตา|ของ|ผู้|ที่|นิยม|เรื่อง|ความ|เป็น|กลาง|ใน|การ|วิจัย| 
sentence = u'เป็นการศึกษาที่ตั้งอยู่บนสมมุติฐานที่ไม่ได้มีลักษณะที่ดีมากนักในสายตาของผู้ที่นิยมเรื่องความเป็นกลางในการวิจัย'
H = HMM()
result = H.pureCut(sentence)
for r in result:
    print r


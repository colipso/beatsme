#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 21:25:25 2017

@author: hp
"""
import sys
import os
sys.path.append("../")
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import codecs

from cutByHMM import HMM

cut = HMM().cut_DAG_NO_HMM

f = codecs.open("thai_new.txt",'r','utf-8')
resultf = codecs.open('thai_new_cut_result.txt' , 'w' , 'utf-8')

cut_result = []

for line in f.readlines():
    cleanLine = line.strip()
    if cleanLine != '':
        for r in cut(cleanLine):
            resultf.write( r+'\n ')
            cut_result.append(r)
     
f.close()
resultf.close()


#right cut

f_right = codecs.open('thai_new_right.txt' , 'r' ,'utf-8')
wrongF1 = codecs.open('thai_new_cut_wrong_cut2right.txt' , 'w' , 'utf-8')
wrongF2 = codecs.open('thai_new_cut_wrong_right2cut.txt' , 'w' , 'utf-8')
right_word = []
for line in f_right.readlines():
    word = line.strip()
    if word != '':
        right_word.append(word)
    

allWordCount = len(right_word)
rightWordCount1 = 0
for w in cut_result:
    if w in right_word:
        rightWordCount1 += 1
    else:
        print w
        wrongF1.write(w + '\n')
        
        
rightWordCount2 = 0
for w in right_word:
    if w in cut_result:
        rightWordCount2 += 1
    else:
        print w
        wrongF2.write(w + '\n')

f_right.close()
wrongF1.close()
wrongF2.close()
print 'The correct rate (cut->right) is %.2f%%' % float(rightWordCount1*100.0/allWordCount)
print 'The news has %d words' % allWordCount
print 'The thaicut tool cut %d words' % len(cut_result)
print 'The news has %d right (cut->right) cuted words' % rightWordCount1
print '\n'
print 'The correct rate (right2cut) is %.2f%%' % float(rightWordCount2*100.0/allWordCount)
print 'The news has %d words' % allWordCount
print 'The thaicut tool cut %d words' % len(cut_result)
print 'The news has %d right (right2cut) cuted words' % rightWordCount2
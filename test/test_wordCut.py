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

for line in f.readlines():
    for r in cut(line):
        resultf.write( r+'\n ')
     
f.close()
resultf.close()
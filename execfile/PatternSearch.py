#-*- coding:utf-8 -*-
__author__ = 'ShdowWalker'

from KeyWordsFilter import *
import codecs

def AbnormalClassClassify(fileName, thershold = 0.005):
    abnormalfeaturedic = readabnormalfeature()
    file = codecs.open(fileName, encoding = 'utf8')
    textstr = file.read()
    # for eachline in file.readlines():
    #     eachline.strip()
    #     if eachline != " ":
    #         textstr = textstr + eachline
    textstr = "".join(textstr.split())
    # print (len(textstr))
    # print(textstr)
    abncount = {}
    maxcount = -1
    maxableng = 0
    maxkey = ""
    for key,val in abnormalfeaturedic.items():
        count = 0
        ableng = 0
        for eachword in val:
            # if eachword in textstr:
            #     count = count + 1
            #     ableng = ableng + len(eachword)
            eachword = eachword.strip()
            if eachword == "" or eachword == " ":
                continue
            eachwordcount = textstr.count(eachword)
            count = count + eachwordcount
            ableng = ableng + len(eachword) * eachwordcount
            # if eachwordcount >= 1:
            #     print (eachword)
            #     print (eachwordcount)

        abncount[key] = count
        if count > maxcount:
            maxcount = count
            # maxkey = key
        if ableng > maxableng:
            maxableng = ableng
            maxkey = key


    isAbn = False
    if float(maxableng) / len(textstr) > thershold:
        # print("maxcount:", maxcount)
        # print (ableng)
        isAbn = True
        return isAbn, maxkey
    else:
        return isAbn, ""



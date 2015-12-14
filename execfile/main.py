#-*- coding:utf-8 -*-
__author__ = 'ShdowWalker'

from TextPreProcess import *
from kmeans import *
from TestFeatureWeight import *

from KeyWordsFilter import *
from PatternSearch import *
import subprocess




classcode = ["汽车", "财经", "IT", "健康", "体育", "旅游", "教育", "招聘", "文化", "军事"]
curPath="execfile/"

def textclassify(filename):
    # abnormalfeaturedic = readabnormalfeature()
    # isabnormalresult, abnormalclassiyres = isabnormal(filename, abnormalfeaturedic)
    isabnormalresult, abnormalclassiyres = AbnormalClassClassify(filename)
    if isabnormalresult:
        print(filename+":不正常, 类别:" + abnormalclassiyres,end='')
    else:
        feature = readFeature(curPath+"SVMFeature.txt")
        dffeaturedic = readDfFeature(curPath+"dffeature.txt")
        calfiletfidf(filename,feature, dffeaturedic)
        filenamesvm = filename.strip(".txt") + ".svm"
        subprocess.call([curPath+"svm-predict.exe", filenamesvm, curPath+"trainscale.model", curPath+"msgclassifyresult.txt"])

        fileresult = open(curPath+"msgclassifyresult.txt", "r")
        filecontent = int(fileresult.read())
        classresult = classcode[filecontent]
        print(filename+":正常, 类别:" + classresult,end='')

# textclassify("msg.txt")

if __name__ == '__main__':
    filename = sys.argv[1]
    textclassify(filename)
    #textclassify('msg.txt')
#-*- coding:utf-8 -*-
__author__ = 'ShdowWalker'
import os
import jieba
import codecs
import chardet


# 对某个文件进行分词,并保存到set中
def cutfiletoset(filename):
    file = codecs.open(filename, "r", encoding = "utf8")
    filecontent = file.read()
    fileseglist = jieba.cut(filecontent)
    filewords = set()
    for eachword in fileseglist:
        filewords.add(eachword)

    # print(len(filewords), filewords)
    return filewords

# 读取文件中的非正常类别的特征

AbnormalCategory = ["暴力类", "政治类", "色情类"]

# 读取得到当前脚本所在的路径
curworkpath = os.path.split(os.path.realpath(__file__))[0]
curfilebase = os.path.join(curworkpath, "Abnormal")

def readabnormalfeature(abnormalcat = AbnormalCategory):
    abnormalfeaturedic = {}

    for i in range(len(abnormalcat)):
        curcat = abnormalcat[i]
        catfilename = os.path.join(curfilebase, abnormalcat[i] + ".txt")
        # print(curcat)
        catfile = codecs.open(catfilename, "r", encoding = "utf8")
        catfilecontent = catfile.read()
        catfeatures = catfilecontent.split("\n")

        # 把list 转换为set
        catfeaturesset = set()
        for eachword in catfeatures:
            catfeaturesset.add(eachword.strip("\r"))
        abnormalfeaturedic[curcat] = catfeaturesset
    # print(abnormalfeaturedic)
    return abnormalfeaturedic


# 判断消息类文本是否非正常

def isabnormal(filename,abnormalfeaturedic, abnormalthershold = 5):
    curfilewords = cutfiletoset(filename)
    # abnormalfeaturedic = readabnormalfeature()

    maxcalsize = -1
    maxcal = ""
    for cat in abnormalfeaturedic:
        catval = abnormalfeaturedic[cat]
        insset = catval & curfilewords
        curcatsize = len(insset)
        # print("当前"+cat, curcatsize)
        if curcatsize > maxcalsize:
            maxcalsize = curcatsize
            maxcal = cat
    # print(maxcal, maxcalsize)
    if maxcalsize > abnormalthershold:
        return True, maxcal
    else:
        return False, None

# 对正常文本进行类别处理(SVM)


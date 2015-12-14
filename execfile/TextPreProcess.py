#-*- coding:utf-8 -*-
__author__ = 'ShdowWalker'
import os
import chardet
import queue
import codecs
import jieba
import math

#
FileCount = 150

# 生成数据文件
def gendatafile(rootdir = "许婷婷"):
    curworkpath = os.path.split(os.path.realpath(__file__))[0]
    # print(curworkpath)
    curdatadir = os.path.join(curworkpath, rootdir)
    datalist = os.listdir(curdatadir)

    traindatadir = os.path.join(curworkpath, "TrainData")
    if os.path.exists(traindatadir):
        pass
    else:
        os.mkdir(traindatadir)
    # 应该深度遍历的
    filecount = 0
    # walk函数遍历文件夹
    for root, dirs, files in os.walk(curdatadir, topdown=True):
        for filename in files:
            # print(os.path.join(root,filename)) # 打印文件绝对路径
            readfilepath = os.path.join(root,filename)
            if filename[-4:] == ".txt":
                readfile = open(readfilepath, "rb")
                fileencoding = chardet.detect(readfile.read())["encoding"]
                # print(fileencoding)
                if fileencoding == "GB2312":
                    fileencoding = "gbk"
                readfile = codecs.open(readfilepath, "r+", fileencoding )
                readfilecontent = readfile.read()
                # print(readfilecontent)
                writefilepath = os.path.join(traindatadir, str(filecount)+".txt")
                writefile = codecs.open(writefilepath,"w+", fileencoding)
                writefile.writelines(readfilecontent)
                readfile.close()
                writefile.close()
                filecount = filecount + 1


# 对数据文件进行分词处理

def cutfile(FileContentCount = FileCount):
    curworkpath = os.path.split(os.path.realpath(__file__))[0]
    curfilebase = os.path.join(curworkpath, "TrainData")
    # print(curfilebase)
    for i in range(FileCount):
        filename = str(i)+".txt"
        curfilename = os.path.join(curfilebase,filename)
        curfile = codecs.open(curfilename, "r", encoding = "gbk")
        curfilecontent = curfile.read()
        seglist = jieba.cut(curfilecontent)
        segcontent = " ".join(seglist)
        writefilepath = os.path.join(curfilebase, str(i)+".cut")
        writefile = codecs.open(writefilepath,"w",encoding = "gbk")
        writefile.write(segcontent)
        curfile.close()
        writefile.close()



# 去除停用词
def ignorestopwords(word):
    stopwordslist = ["的", "我们","要","自己","之","将","“","”","，","（","）","后","应","到","某","后","个","是","位","新","一","两","在","中","或","有","更","好"," "]
    if word in stopwordslist:
        return True
    else:
        return False

# 统计得到训练数据中去除停用词后的向量
def calallthewords(FileContentCount = FileCount):
    curworkpath = os.path.split(os.path.realpath(__file__))[0]
    curfilebase = os.path.join(curworkpath, "TestKmeans")

    # 得到所有文件的特征向量
    allfilevector = set()
    # 建立每个文件对其单词向量去除停用词的映射
    fileworddic = {}
    for i in range(FileCount):
        # filename = str(i)+".cut"
        filename = str(i)+".cut"
        curfilepath = os.path.join(curfilebase, filename)
        readcutfile = open(curfilepath, "r", encoding = "gbk")
        curfilecontent = readcutfile.read().split(" ")
        # 去除停用词后的向量
        curfilewordslist = []
        for eachword in curfilecontent:
            if not ignorestopwords(eachword):
                allfilevector.add(eachword)
                curfilewordslist.append(eachword)
        readcutfile.close()
        fileworddic[i] = curfilewordslist
    allwordslist = list(allfilevector)
    # print("allwordlist: ", allwordslist)
    return allwordslist, fileworddic



# 文本聚类中特征选择
def featureselection():
    pass



# TF IDF 计算
def TFIDF(FileContentCount = FileCount):

    # 计算TF
    allwordlist, fileworddic = calallthewords(FileContentCount)
    # print(len(allwordlist))
    filetfdic = {}  # filetfdic为这样的字典,键为文件名值为字典，值的字典每个键为词，值为词的tf
    for filekey in fileworddic:
        filewordlist = fileworddic[filekey]
        curfiletf = {}
        for eachword in filewordlist:
            if eachword not in curfiletf.keys():
                curfiletf[eachword] = 1 # 当初脑抽为什么设为0
            else:
                curfiletf[eachword] = curfiletf[eachword] + 1
        # print(filekey, curfiletf)
        for eachwordkey in curfiletf:
            curfiletf[eachwordkey] = float(curfiletf[eachwordkey]) / len(fileworddic[filekey])
        filetfdic[filekey] = curfiletf

    # 计算IDF
    # 对每个文件中的每个词进行遍历
    totaldocumentsize = len(fileworddic)
    # print("文本数目", totaldocumentsize)
    fileidfdic = {}
    for filekey in filetfdic:
        filekeyvalue = filetfdic[filekey]
        curfileidf = {}
        for eachwordkey in filekeyvalue:
            curworddocount = 0
            for anotherfilekey in filetfdic:
                if eachwordkey in filetfdic[anotherfilekey].keys():
                    curworddocount = curworddocount + 1
            curwordidf = math.log(float(totaldocumentsize)/float(curworddocount))
            curfileidf[eachwordkey] = curwordidf
        fileidfdic[filekey] = curfileidf

    #合并计算得到TF-IDF
    filetfidfdic = {}
    for filekey in fileidfdic:
        curfiletfidf = {}
        for eachword in allwordlist:
            curfiletfidf[eachword] = 0.0
        filetfidfdic[filekey] = curfiletfidf

    for filekey in filetfdic:
        filekeyvalue = filetfdic[filekey]
        for eachword in filekeyvalue:
            curwordtfidf = filekeyvalue[eachword] * fileidfdic[filekey][eachword] # 我在这里扩大10倍
            filetfidfdic[filekey][eachword] = curwordtfidf


    # 把filetfidfdic 转化为filetfidfdiclist
    allwordlist.sort()
    # print(allwordlist)
    filetfidfdiclist = {}
    for filekey in filetfidfdic:
        lis = [0] * len(allwordlist)
        filetfidfdiclist[filekey] = lis

    for filekey in filetfidfdic:
        filekeyvalue = filetfidfdic[filekey]
        for eachword in filekeyvalue:
            wordindex = allwordlist.index(eachword)
            filetfidfdiclist[filekey][wordindex] = filekeyvalue[eachword]
    return filetfidfdiclist

















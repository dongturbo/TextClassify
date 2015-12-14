#-*- coding:utf-8 -*-
__author__ = 'ShdowWalker'
import math
import random

# kmeans 聚类算法实现

# 计算向量之间的Cosine距离

def cosdistance(list1, list2):
    if len(list1) == len(list2):
        nume = 0.0
        a1 = 0.0
        b1 = 0.0
        for i in range(len(list1)):
            nume = nume + list1[i] * list2[i]
            a1 = a1 + list1[i] * list1[i]
            b1 = b1 + list2[i] * list2[i]
        demo = (math.sqrt(a1) * math.sqrt(b1))
        # print(nume, demo)
        result = 1.0-float(nume)/ float(demo) # 为什么会有float diversion zero error
        # print ("distance：", result)
        return result
    else:
        print("error length is not equal")

# 求Cluster的centroid (随机取值)
def randclustercentroid(dataset):
    # 得到dataset的每一维的最大值与最小值
    MaxF = float("inf")
    MinF = - float("inf")
    dimsize = len(list(dataset.values())[0])
    minlist = [MaxF] * dimsize
    maxlist = [MinF] * dimsize

    for filekey in dataset:
        filekeyvalue = dataset[filekey]
        for i in range(len(filekeyvalue)):
            if filekeyvalue[i] < minlist[i]:
                minlist[i] = filekeyvalue[i]
            if filekeyvalue[i] > maxlist[i]:
                maxlist[i] = filekeyvalue[i]

    # 可以在某一范围内随机生成centroids
    # centroids = {}
    # for j in range(k):
    #     centroids[j] = [0.0] * dimsize
    # for j in range(k):
    #     for l in range(dimsize):
    #         centroids[j][l] = random.uniform(minlist[l], maxlist[l])
    centroid = [0.0] * dimsize
    for l in range(dimsize):
        centroid[l] = random.uniform(minlist[l], maxlist[l])

    return centroid

# 求cluster的中心
def clustercentroid (clusters, dataset):
    centroids = {}
    for key in clusters:
        cluster = clusters[key]
        if len(cluster) == 0:
            centroids[key] = randclustercentroid(dataset)
        else:
            sumlist = [0.0] * len(list(dataset.values())[0])
            for eachitem in cluster:
                for i in range(len(dataset[eachitem])):
                    sumlist[i] = sumlist[i] + dataset[eachitem][i]

            for i in range(len(sumlist)):
                sumlist[i] = sumlist[i] / len(cluster)
            # print("cluster", key , " :" , sumlist)
            centroids[key] = sumlist

    return centroids


# KMeans 算法实现
def kmeans(dataset , k = 2, disMeas = cosdistance, creatCent = clustercentroid):
    docassiment = {}
    clusters = {}
    for i in range(k):
        lis = []
        clusters[i] = lis
    # 确定文档的初始划分
    for dockey in dataset:
        clusterindex = random.randint(0, k-1)
        clusters[clusterindex].append(dockey)
        docassiment[dockey] = clusterindex
    print("Inital Cluster", clusters)
    centroids = creatCent(clusters, dataset) # 计算聚类中心
    clusterchanged = True
    count = 0
    while clusterchanged:
        print("while loop: " +str(count))
        clusterchanged = False
        # 寻找最近的质心
        for dockey in dataset:
            docvec = dataset[dockey]
            minindex = -1
            Mindis = float("inf")
            for j in range(k):
                curdis = disMeas(docvec, centroids[j])
                # print("curdis", curdis ," j" , j)
                if curdis < Mindis:
                    minindex = j
                    Mindis = curdis
            # print("dockey:", dockey, "minindex:", minindex, "docassiment[dockey]:", docassiment[dockey])
            if docassiment[dockey] != minindex:
                print("cluster changed")
                clusterchanged = True
                originindex = docassiment[dockey]
                clusters[originindex].remove(dockey)
                clusters[minindex].append(dockey)
                # print("clusters:" , clusters)
                docassiment[dockey] = minindex

        centroids = clustercentroid(clusters, dataset)
        count = count + 1
    return clusters











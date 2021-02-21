import copy
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from math import sqrt
import pandas as pd
import matplotlib.pyplot as plt


chartPath = "D:/py/AI-coach-Server/data/runningChart/"

# 分割测试数据(times动作次数)
# 返回综合评价折线图
def segTest(standardList, testList, times):
    # 对标准动作，
    temp = copy.deepcopy(standardList)
    for i in range(times - 1):
        for j in range(len(temp)):
            standardList.append(temp[j])
    path = fastDtw(
        testList, standardList
    )  ###test在前，tuple中为横坐标,distance:dtw距离，path:dtw路径
    proposal = DrawChart(times, testList, standardList, path)  # 返回建议
    return proposal


# runningList与standardList等长，规范，动作可以通过索引识别
# 返回的数组对应部位：头颈，左肩臂，左肘，右肩臂，右肘，左胯，左膝，左脚踝，右胯，右膝，右脚踝
def DrawChart(times, testList, standardList, path):
    # testList与standardList长度不等，二者进行对齐
    runningTestList, runningStandardList = alignedList(testList, standardList, path)
    # 开始画图
    disList = getDisList(runningTestList, runningStandardList)
    df = pd.DataFrame(disList, index=range(len(runningStandardList)))
    df.plot()
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig(chartPath + "evaluationResult.jpg")
    plt.close()
    # 部位评价
    partEvaluation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(runningTestList[0])):
        for j in range(len(runningTestList)):
            partEvaluation[i] += abs(runningTestList[j][i] - runningStandardList[j][i])
    return partEvaluation


# 根据path进行对齐
def alignedList(testList, standardList, path):
    runningTestList = []
    runningStandardList = []
    ix = 0
    ixNext = 1
    while ixNext < len(path):
        if path[ix][0] != path[ixNext][0] and path[ix][1] != path[ixNext][1]:
            runningTestList.append(testList[path[ix][0]])
            runningStandardList.append(standardList[path[ix][1]])
            ix += 1
            ixNext += 1
        elif path[ix][0] == path[ixNext][0]:
            while ixNext < len(path) and path[ix][0] == path[ixNext][0]:
                ixNext += 1
            runningTestList.append(testList[path[ix][0]])
            runningStandardList.append(
                calMean(standardList, path[ix][1], path[ixNext - 1][1])
            )
            ix = ixNext
            ixNext += 1
        elif path[ix][1] == path[ixNext][1]:  # path[ix][1] == path[ixNext][1]
            while ixNext < len(path) and path[ix][1] == path[ixNext][1]:
                ixNext += 1
            runningTestList.append(calMean(testList, path[ix][0], path[ixNext - 1][0]))
            runningStandardList.append(standardList[path[ix][1]])
            ix = ixNext
            ixNext += 1
    return runningTestList, runningStandardList


# 得到测试与标准间的距离用于画图
def getDisList(runningList, standardList):
    result = []
    for i in range(len(runningList)):
        result.append(getDis(runningList[i], standardList[i]))
    return result


# 得到两个帧对应的特征向量之间的距离
def getDis(r, s):
    result = 0
    for i in range(len(r)):
        result += (r[i] - s[i]) ** 2
    return sqrt(result)


# 找出测试数据中冗余的部分，用于计算平均
def findRedundancy(path):
    needMeanList = []
    lastidx = 0
    idx = 1
    while idx < len(path):
        if path[idx][1] == path[lastidx][1]:
            while idx < len(path) and path[idx][1] == path[lastidx][1]:
                idx += 1
            needMeanList.append((lastidx, idx - 1))
            lastidx = idx - 1
        idx += 1
        lastidx += 1
    return needMeanList


# 对于List从start到end进行平均值计算
def calMean(List, start, end):
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    div = end - start + 1
    while start <= end:
        for i in range(11):
            result[i] += List[start][i]
        start += 1
    for i in range(11):
        result[i] = result[i] / div
    return result


# 11个特征向量值分别计算平均值
def getMean(testList, x, y):
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    idx = x
    for i in range(len(testList[0])):
        for j in range(x, y + 1):
            result[i] += testList[j][i]
        result[i] /= y - x + 1
    return result


# 动态规整
def fastDtw(testList, standardList):
    distance, path = fastdtw(testList, standardList, dist=euclidean)
    return path
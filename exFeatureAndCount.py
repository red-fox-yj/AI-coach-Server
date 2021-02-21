import os
import json
import numpy as np
from coordinate_2D import coor_2D

# 如果不用头而用其他部位的话就再加一个参数，judgeState的值可以用动作需要参数对应的数组来给定，再加的参数也是
# isRunning用来判断调用这个函数的json是否是要用于评价的，如果不是，则不需要getCount得到个数和能量，类似重用
def exFeaturefrom2Djson(runningPath, judgeState="", isRunning=False):
    origList = []
    countList = []
    files = os.listdir(runningPath)  # 读取一个文件夹下所有json文件
    for file in files:
        if not os.path.isdir(file) and file.endswith(".json"):
            with open(runningPath + "" + file, mode="r") as fd:
                temp_dict = json.load(fp=fd)
                if len(temp_dict["people"]):  # 判断图像中是否识别出了人
                    temp_list = temp_dict["people"][0]["pose_keypoints_2d"]
                    origList.append(temp_list)
                    countList.append(temp_list[1])
    if isRunning:
        W = getCountW(countList, judgeState)
        return exFeature(origList), exFeatureXY(origList), W
    else:
        return exFeature(origList)  # 返回各帧的部位角度组


# 得到计数
def getCountW(meanposls, judgeState):
    # 判定目前方向的列表
    dirls = []
    # 窗口平均值
    revisels = []
    # 顶点列表
    summitls = []
    # 波谷列表
    troughls = []
    # 设置一个滑动窗口
    slide_win = 3
    # 总共走得长度
    W = 0
    framecnt = len(meanposls)
    # 计算做功
    for t in range(1, len(meanposls)):
        W += np.abs(meanposls[t] - meanposls[t - 1])

    for ix, va in enumerate(meanposls):
        if ix == len(meanposls) - 1:
            break
        else:
            dir = "up" if meanposls[ix + 1] - meanposls[ix] < 0 else "down"
            dirls.append(dir)
    # # 去抖动
    # for ix in range(1, len(dirls) - 1):
    #     if (dirls[ix] != dirls[ix - 1]) and (dirls[ix] != dirls[ix + 1]) and (dirls[ix - 1] == dirls[ix + 1]):
    #         revisels.append(ix)
    # for each in revisels:
    #     dirls[each] = dirls[each - 1]
    # print(dirls)

    return W


# 从一个原始动作序列中提取特征序列
def exFeature(origList):
    featureList = []
    for aAction in origList:
        featureList.append(exFeatureFromStd(standardizeAction(aAction)))
    return featureList


# 从一个原始动作序列中提取特征序列
def exFeatureXY(origList):
    featureXY = []
    for aAction in origList:
        featureXY.append(standardizeAction(aAction))
    return featureXY


# 标准化一个动作，没有置信度处理(对25个身体部位进行坐标处理)
def standardizeAction(aAction):
    standardList = []
    coorcnt = 0
    x = 0.0
    y = 0.0

    for cor in aAction:
        if 0 == coorcnt:
            x = cor
            coorcnt += 1
            continue
        if 1 == coorcnt:
            y = cor
            coorcnt += 1
            continue
        if 2 == coorcnt:
            standardList.append(coor_2D(x, y))
            coorcnt = 0
            continue
    return standardList


# 从一个标准化动作中提取特征向量
# 没有解决的问题：有的点检测不到，为零，甚至连续检测不到，无法得到cos值
def exFeatureFromStd(aStdAction):
    featureList = []
    body = []
    # 部位向量值
    body.append(aStdAction[18] - aStdAction[17])  # 头部
    body.append(aStdAction[1] - aStdAction[0])  # 颈部
    body.append(aStdAction[5] - aStdAction[2])  # 肩膀
    body.append(aStdAction[6] - aStdAction[5])  # 左上臂
    body.append(aStdAction[7] - aStdAction[6])  # 左前臂
    body.append(aStdAction[3] - aStdAction[2])  # 右上臂
    body.append(aStdAction[4] - aStdAction[3])  # 右前臂
    body.append(aStdAction[12] - aStdAction[9])  # 髋部
    body.append(aStdAction[13] - aStdAction[12])  # 左大腿
    body.append(aStdAction[14] - aStdAction[13])  # 左小腿
    body.append(aStdAction[19] - aStdAction[14])  # 左脚
    body.append(aStdAction[10] - aStdAction[9])  # 右大腿
    body.append(aStdAction[11] - aStdAction[10])  # 右小腿
    body.append(aStdAction[22] - aStdAction[11])  # 右脚
    # 计算部位之间角度
    featureList.append(body[1].cos_2D(body[0]))  # 头颈
    featureList.append(body[3].cos_2D(body[2]))  # 左肩臂
    featureList.append(body[4].cos_2D(body[3]))  # 左肘
    featureList.append(body[5].cos_2D(body[2]))  # 右肩臂
    featureList.append(body[6].cos_2D(body[5]))  # 右肘
    featureList.append(body[8].cos_2D(body[7]))  # 左胯
    featureList.append(body[9].cos_2D(body[8]))  # 左膝
    featureList.append(body[10].cos_2D(body[9]))  # 左脚踝
    featureList.append(body[11].cos_2D(body[7]))  # 右胯
    featureList.append(body[12].cos_2D(body[11]))  # 右膝
    featureList.append(body[13].cos_2D(body[12]))  # 右脚踝

    return featureList


if __name__ == "__main__":
    runningPath = "./data/runningJson/"
    print(exFeaturefrom2Djson(runningPath))
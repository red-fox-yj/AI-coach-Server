import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from exFeatureAndCount import exFeaturefrom2Djson
from dtwSegAndDraw import segTest
from argparser import parser
from act_list import string_to_num
import matplotlib.pyplot as plt

partStandard = 50
standardPath = "D:/py/Ai-coach01/standard/"
commandActivate = "activate tensorflow"
commandDeactivate = "conda deactivate"
Font = r"D:/py/Ai-coach01/data/font/楷体_GB2312.ttf"  # 指定字体
bodyPart = ["头颈", "左肩臂", "左肘", "右肩臂", "右肘", "左胯", "左膝", "左脚踝", "右胯", "右膝", "右脚踝"]

# 绘图生成报告
def drawPic(Court, energy):
    print("drawPic")
    # 原图路径
    pic = "D:/py/Ai-coach01/data/runningReport/report_default.png"
    # 保存路径
    path = "D:/py/Ai-coach01/data/runningReport/" + call_args.report_name + ".png"
    # 打开初始文件
    image = Image.open(pic)
    font = ImageFont.truetype(Font, 70)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    site = (120, 200)  # 距离左上角距离
    txt = "编号：" + call_args.report_name  # 填充文字
    draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)

    site = (120, 350)  # 距离左上角距离
    txt = "计数：" + str(Court) + "个"  # 填充文字
    draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)

    site = (120, 650)  # 距离左上角距离
    txt = "能量：" + str(energy) + "焦耳"  # 填充文字
    draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)

    score = 11
    result = ""
    size = 0
    height = 950
    if call_args.mode_choose == "mode_2":  # mode_2动作评估
        for i in range(len(proposal)):
            if proposal[i] > Court * partStandard:
                score = score - 1
        site = (120, 800)  # 距离左上角距离
        txt = "继续加油哦！"  # 填充文字
        draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)
    else:  # mode_1姿态纠正
        site = (120, 800)  # 距离左上角距离
        txt = "您需要注意的地方是："  # 填充文字
        draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)

        for i in range(len(proposal)):
            if proposal[i] > Court * partStandard:
                score = score - 1
                result += bodyPart[i] + "，"
                size = size + 1
                if size == 3:  # 每三个部位换一次行
                    site = (120, height)  # 距离左上角距离
                    txt = result  # 填充文字
                    draw.text(
                        site, txt, font=font, fill="#000", stroke_width=1
                    )  # 输出文字(可以连续写入)
                    height = height + 150
                    size = 0
                    result = ""
        # 再写一次防止漏掉不满足整三的部位
        site = (120, height)  # 距离左上角距离
        txt = result  # 填充文字
        draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)
        if score == 11:  # 若动作标准
            site = (120, 950)  # 距离左上角距离
            txt = "动作标准，请再接再厉！"  # 填充文字
            draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)

    site = (120, 500)  # 距离左上角距离
    txt = "得分：" + str(round((score / 11) * 100, 2))  # 填充文字
    draw.text(site, txt, font=font, fill="#000", stroke_width=1)  # 输出文字(可以连续写入)
    print("得分" + str(round((score / 11) * 100, 2)))

    # 模糊并保存:
    image.filter(ImageFilter.BLUR)
    image.save(path)


# 部位编号列表
# {0,  "Nose"},
# {1,  "Neck"},
# {2,  "RShoulder"},
# {3,  "RElbow"},
# {4,  "RWrist"},
# {5,  "LShoulder"},
# {6,  "LElbow"},
# {7,  "LWrist"},
# {8,  "MidHip"},
# {9,  "RHip"},
# {10, "RKnee"},
# {11, "RAnkle"},
# {12, "LHip"},
# {13, "LKnee"},
# {14, "LAnkle"},
# {15, "REye"},
# {16, "LEye"},
# {17, "REar"},
# {18, "LEar"},
# {19, "LBigToe"},
# {20, "LSmallToe"},
# {21, "LHeel"},
# {22, "RBigToe"},
# {23, "RSmallToe"},
# {24, "RHeel"},
# {25, "Background"}

# 读入list,根据部位编号，计算波峰个数
def WaveGet(pointXYlist, part, name):
    number = 0
    featureYP = []
    for i in range(len(pointXYlist)):
        featureYP.append(pointXYlist[i][part].y)  # 常规的动作一般为克服重力做功

    print("波形图点Y坐标")
    print(featureYP)
    # 绘图
    df = pd.DataFrame(featureYP, index=range(len(featureYP)))
    df.plot()
    ax = df.plot()
    fig = ax.get_figure()
    if os.path.exists("D:/py/Ai-coach01/data/partYchart/" + name) == False:
        os.mkdir("D:/py/Ai-coach01/data/partYchart/" + name)  # 创建目录
    fig.savefig("D:/py/Ai-coach01/data/partYchart/" + name + "/" + str(part) + ".jpg")
    plt.close()

    mid = (max(featureYP) + min(featureYP)) / 2
    print("中值")
    print(mid)
    for i in range(len(featureYP) - 1):
        if (featureYP[i] - mid) * (featureYP[i + 1] - mid) < 0:  # 存在一个交点
            number = number + 1

    return number / 2


if __name__ == "__main__":

    call_args = parser.parse_args()
    # 生成的json文件目录
    runningPath = "D:/py/Ai-coach01/data/runningJson/" + call_args.report_name + "/"
    # 生成的图表文件目录
    chartPath = "D:/py/Ai-coach01/data/runningChart/" + call_args.report_name + "/"
    # 生成的报告文件目录
    reportPath = "D:/py/Ai-coach01/data/runningReport/" + call_args.report_name + "/"
    # 启动openpose命令
    commandGenerateJson = (
        r"bin\OpenPoseDemo.exe --video D:\py\Ai-coach01\data\test"
        + "\\"
        + call_args.report_name
        + ".avi  --write_json D:/py/Ai-coach01/data/runningJson"
        + "/"
        + call_args.report_name
    )
    # 命令合成
    command = (
        commandActivate + " && " + commandGenerateJson + " && " + commandDeactivate
    )
    activity = call_args.activity_choose

    # 调用控制台命令
    os.chdir("D:\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose")
    os.system(command)

    nowStandardPath = standardPath + activity + "/"  # 通过读取客户端发来的消息
    featureRunning, featureXYRunning, W = exFeaturefrom2Djson(runningPath, "up", True)

    parts_statistics = []
    # 部位折线图预估次数
    count = WaveGet(
        featureXYRunning,
        string_to_num(call_args.activity_choose),
        call_args.report_name,
    )

    if count > 0:
        featureStandard = exFeaturefrom2Djson(nowStandardPath)
        proposal = segTest(featureStandard, featureRunning, int(count))
        print("建议数组")
        print(proposal)
        print("运动次数")
        print(round(count))
        print("消耗能量")
        print(round(W, 2))
        drawPic(round(count), round(W, 2))

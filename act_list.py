#根据动作返回波峰采集部位编号
def string_to_num(activity):
    numbers = {
        "squat" : 0,#下蹲——0——“鼻子”
        #在此添加其他动作

    }

    return numbers.get(activity,None)

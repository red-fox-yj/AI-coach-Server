'''命令行解析模块'''
import argparse

parser = argparse.ArgumentParser(  # 建立解析对象
    description="2D json files were parsed and the test video was decomposed into single segment by using DTW.")

parser.add_argument(
    "-n"
    , "--name"  # 处理视频和反馈报告的名称
    , required=True  # 必须
    , type=str
    , dest="report_name"  # 选项关联到一个特定的名字
    , help="Process the name of the video and feedback report"
)

parser.add_argument(
    "-a"
    , "--activity"  # 动作选择
    , required=True  # 必须
    , type=str
    , dest="activity_choose"
    , help="Accept the action selected by the user"
)

parser.add_argument(
    "-m"
    , "--mode"  # 模式选择
    , required=True  # 必须int
    , type=str
    , dest="mode_choose"
    , help="Accept the action selected by the user"
)
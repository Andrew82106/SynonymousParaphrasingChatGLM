"""
信息输出模块，包括INFO，DEBUG，WARNING模块
"""
import time
import os
import inspect

InfoLevel = 1
# 信息等级，大于该等级的信息不输出
# 0级信息为重要信息，必须输出
defaultLevel = 2


def calcTime():
    current_timestamp = time.time()
    current_time_struct = time.localtime(current_timestamp)
    current_date = time.strftime("%Y-%m-%d", current_time_struct)
    current_time = time.strftime("%H:%M:%S", current_time_struct)
    return f"{current_date}\t{current_time}"


def getThisInSTACK():
    caller_frame = inspect.currentframe().f_back
    caller_filename = inspect.getframeinfo(caller_frame).filename
    caller_lineno = inspect.getframeinfo(caller_frame).lineno
    return caller_filename, caller_lineno


def INFO(TextIn, level=defaultLevel):
    if level > InfoLevel:
        return
    caller_filename, caller_lineno = getThisInSTACK()
    print(f"[INFO]\tin file {os.path.basename(caller_filename)}(line {caller_lineno})\t{calcTime()}: {TextIn}")


def DEBUG(TextIn, level=defaultLevel):
    if level > InfoLevel:
        return
    caller_filename, caller_lineno = getThisInSTACK()
    print(f"[DEBUG]\tin file {os.path.basename(caller_filename)}(line {caller_lineno})\t{calcTime()}: {TextIn}")


def WARNING(TextIn, level=defaultLevel):
    if level > InfoLevel:
        return
    caller_filename, caller_lineno = getThisInSTACK()
    print(f"[WARNING]\tin file {os.path.basename(caller_filename)}(line {caller_lineno})\t{calcTime()}: {TextIn}")


if __name__ == '__main__':
    INFO("load model")
    DEBUG("load model")
    WARNING("load model")

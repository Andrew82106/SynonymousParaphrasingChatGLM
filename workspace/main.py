# -*- coding:UTF-8 -*-

import json
import argparse
from configs.pathcfg import Pcfg
parser = argparse.ArgumentParser(description='Parameters for pretraining')
parser.add_argument('--task', choices=["single", "batches"], dest='TASK', help='task name, e.g., ok, aok_val, aok_test', type=str, default="single")
parser.add_argument('--savepath', dest='SAVEPATH', help='task name, e.g., ok, aok_val, aok_test', type=str, default=Pcfg.jsonPath + "/debug1.json")
args = parser.parse_args()
TASK = args.TASK
savepath = args.SAVEPATH
print(f"[para config]:\n[TASK]={TASK}\n[savepath]={savepath}\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


import pprint
import tqdm
from models import promptMain
from Utils.load_model import chatglm
from Utils.debugformat import INFO, DEBUG, WARNING


class Runner:
    """
    实现模型接口。调用Run方法就可以对文本进行分析，调用RunInBatches方法就可以对样本进行批量分析
    """
    def __init__(self):
        self.model = chatglm()

    @staticmethod
    def savefile(savePath, res):
        if savePath is None:
            savePath = Pcfg.jsonPath + "/debug.json"
        INFO(f"运行结果保存至{savePath}")
        with open(savePath, "w", encoding='utf-8') as f:
            json.dump(res, f)

    def Run(self, Text, savePath=None):
        backCar = '\n'
        space = ' '
        INFO(
            f"启用单文本分析模式，文本长度:{len(Text)}，文本摘要:{Text.replace(backCar, '').replace(space, '')[:10]}",
            level=0
        )
        res = promptMain.process(Text=Text, model=self.model)
        self.savefile(savePath, res)
        return res

    def RunInBatches(self, TextList, savePath=None):
        INFO(
            f"启用多文本分析模式，共{len(TextList)}文本",
            level=0
        )
        res = {}
        cnt = 1
        for i in TextList:
            INFO(
                f"分析文本({cnt}/{len(TextList)})\n",
                level=0
            )
            res[i] = promptMain.process(Text=i, model=self.model)
            cnt += 1
            self.savefile(savePath, res)
        return res

    def checkModel(self):
        checkQuestion = "讲一下机器人三大定律"
        Response = self.model.response(checkQuestion)
        DEBUG(f"Checking ChatGLM model\n\tQuestion: {checkQuestion}\n\tResponse: {Response[0]}")
        if Response[0] == -1:
            WARNING("Fail to check model, error messages are below")
            raise Response[1]
        else:
            INFO("model works fine!!!")


if __name__ == '__main__':
    A = Runner()
    if TASK == "single":
        with open(Pcfg.input + '/single.txt', "r", encoding='utf-8') as f:
            content = f.read()
            A.Run(content, savePath=savepath)
    elif TASK == 'batches':
        with open(Pcfg.input + '/batches.txt', "r", encoding='utf-8') as f:
            content = f.read()
            lst = str(content).split("\n")
            A.RunInBatches(lst, savePath=savepath)
            INFO(f"完成批量分析(样本量:{len(lst)})")

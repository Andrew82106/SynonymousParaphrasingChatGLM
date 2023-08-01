"""
CEC dataset format:
{
    sample id: {
        'content': str,
        'event_id': {
            'id1': 'event description1',
            'id2': 'event description2'
        },
        'relation':
            [
                [event_id1, event_id1, relationship1],
                [event_id2, event_id2, relationship2]
            ]

    }
}
"""

import json
import time
import tqdm
from Evaluate import Evaluate
CECRoute = "../output/json/CEC.json"
with open(CECRoute, "r", encoding='utf-8') as f:
    cec = json.load(f)

rawRoute = "./raw_json.json"
with open(rawRoute, "r", encoding='utf-8') as f:
    raw = json.load(f)


class EvaluateOnCEC(Evaluate):
    def __init__(self):
        super(EvaluateOnCEC, self).__init__(CECRoute, rawRoute, cec, raw)
        self.relationshipList = ['Causal']
        self.aimRelation = ['Causal']

    def evaluate(self):
        self.formatData()
        time.sleep(1)
        print("[Evaluate] 数据集: CEC_事件提取")
        print("[Evaluate] 判断文本相同相似度阈值: {}".format(self.eps))
        print("[Evaluate] 成功分析的样本占比: {:.2f}%".format(self.sucRate()))
        print("[Evaluate] 事件抽取关注的样本事件类型: {}".format(self.relationshipList))
        print("[Evaluate] 事件抽取 F1: {:.2f}".format(self.F1()))
        print("[Evaluate] 关系分析关注的样本事件类型: {}".format(self.aimRelation))
        print("[Evaluate] 关系分析 F1: {:.2f}".format(self.F1_relationship()))

    def formatData(self):
        newJson = {}
        for i in self.rawJson:
            if self.rawJson[i] == -1:
                continue  # 有误的信息直接筛掉
            try:
                newJson_i = {
                    'content': i,
                    'event_id': {},
                    'relation': []
                }
                event_cnt = 0
                for j in self.rawJson[i]['顺承关系']:
                    event1 = j['前一事件']['事件描述'] if "->" not in j else j.split("->")[0]
                    newJson_i['event_id'][f'e{event_cnt}'] = event1
                    event_cnt += 1
                    event2 = j['后一事件']['事件描述'] if "->" not in j else j.split("->")[1]
                    newJson_i['event_id'][f'e{event_cnt}'] = event2
                    newJson_i['relation'].append([f'e{event_cnt-1}', f'e{event_cnt}', 'Follow'])
                    event_cnt += 1
                for j in self.rawJson[i]['因果关系']:
                    event1 = j['原因']['事件描述'] if "->" not in j else j.split("->")[0]
                    newJson_i['event_id'][f'e{event_cnt}'] = event1
                    event_cnt += 1
                    event2 = j['结果']['事件描述'] if "->" not in j else j.split("->")[1]
                    newJson_i['event_id'][f'e{event_cnt}'] = event2
                    newJson_i['relation'].append([f'e{event_cnt - 1}', f'e{event_cnt}', 'Causal'])
                    event_cnt += 1
                newJson[i] = newJson_i
            except Exception as e:
                pass
        self.newJson = newJson

    def sucRate(self):
        return 100 * (len(self.newJson) / len(self.rawJson))

    def F1(self):
        """
        计算事件抽取效果相关指标
        """
        P = []
        # P :待检测样本中正确预测的样本数/待检测样本中总样本数为正确率
        R = []
        # R :答案样本中正确预测的样本数/答案样本中总样本数为召回率
        time.sleep(1)
        for sample in tqdm.tqdm(self.newJson, desc="对分析成功的有效文本进行验证"):
            sample = self.newJson[sample]
            description = sample['content']
            for ans in self.BaseJson:
                ans = self.BaseJson[ans]
                if ans['content'] == description:
                    # 找到了对应的origin文本
                    eventLst = []
                    ansEventLst = []
                    """
                    for event_id in sample['event_id']:
                        event = sample['event_id'][event_id]
                        eventLst.append(event)
                    
                    # 获取所有关系相关的事件
                    for ansEvent_id in ans['event_id']:
                        ansEvent = ans['event_id'][ansEvent_id]
                        ansEventLst.append(ansEvent)
                    """
                    # 获取relationshipList中关系相关的事件

                    for relationI in sample['relation']:
                        if relationI[2] in self.relationshipList:
                            eventLst.append(sample['event_id'][relationI[0]])
                            eventLst.append(sample['event_id'][relationI[1]])
                    eventLst = list(set(eventLst))


                    for relationI in ans['relation']:
                        if relationI[2] in self.relationshipList:
                            ansEventLst.append(ans['event_id'][relationI[0]])
                            ansEventLst.append(ans['event_id'][relationI[1]])
                    ansEventLst = list(set(ansEventLst))
                    """
                    # 计算精确度召回率和F1值的旧方法
                    len_raw = len(eventLst)
                    len_ans = len(ansEventLst)
                    for i in eventLst:

                        maxx = -1
                        maxxContent = ''
                        for j in ansEventLst:
                            likelyHood = self.likelyHood(i, j)
                            if likelyHood > maxx:
                                maxx = likelyHood
                                maxxContent = j

                        if maxx > self.eps:
                            eventLst.remove(i)
                            ansEventLst.remove(maxxContent)
                    P.append((len_raw - len(eventLst))/len_raw)
                    R.append((len_ans - len(ansEventLst))/len_ans)
                    """
                    # 计算精确度召回率和F1值的新方法
                    visEventLst = [0 for i in range(len(eventLst))]
                    visAnsEventLst = [0 for i in range(len(ansEventLst))]
                    for i in range(len(eventLst)):
                        for j in range(len(ansEventLst)):
                            likelyHood = self.likelyHood(eventLst[i], ansEventLst[j])
                            if likelyHood > self.eps:
                                visEventLst[i] = 1
                                visAnsEventLst[j] = 1

                    if len(visEventLst):
                        P_i = sum(visEventLst) / len(visEventLst)
                        P.append(P_i)

                    if len(visAnsEventLst):
                        R_i = sum(visAnsEventLst)/len(visAnsEventLst)
                        R.append(R_i)
                    break

        P = 0 if len(P) == 0 else sum(P)/len(P)
        R = 0 if len(R) == 0 else sum(R)/len(R)
        print("[RESULT] 事件抽取 Precision:{:.2f}".format(P))
        print("[RESULT] 事件抽取 Recall:{:.2f}".format(R))
        return 0 if (P == 0 or R == 0) else 2*P*R/(P+R)

    def F1_relationship(self):
        """
        计算关系分析效果相关指标
        """
        P = []
        # P :待检测样本中正确预测的样本数/待检测样本中总样本数为正确率
        R = []
        # R :答案样本中正确预测的样本数/答案样本中总样本数为召回率
        time.sleep(1)
        for sample in tqdm.tqdm(self.newJson, desc="对分析成功的有效文本进行验证"):
            sample = self.newJson[sample]
            description = sample['content']
            for ans in self.BaseJson:
                ans = self.BaseJson[ans]
                if ans['content'] == description:
                    # 找到了对应的origin文本
                    relaLst = []
                    ansrelaLst = []
                    for relationship in sample['relation']:
                        if relationship[2] in self.aimRelation:
                            relaLst.append([relationship[0], relationship[1]])

                    for relationship in ans['relation']:
                        if relationship[2] in self.aimRelation:
                            ansrelaLst.append([relationship[0], relationship[1]])
                    vis_relaLst = [0 for i in range(len(relaLst))]
                    vis_ansrelaLst = [0 for i in range(len(ansrelaLst))]

                    for i in range(len(relaLst)):
                        for j in range(len(ansrelaLst)):
                            # if self.likelyHood(relaLst[i][0] + relaLst[i][1], ansrelaLst[j][0] + ansrelaLst[j][1]) > self.eps:
                            # if self.likelyHood(relaLst[i][0], ansrelaLst[j][0]) > self.eps and self.likelyHood(relaLst[i][1], ansrelaLst[j][1]) > self.eps:
                            if self.likelyHood(relaLst[i][0], ansrelaLst[j][0]) > self.eps and self.likelyHood(relaLst[i][1], ansrelaLst[j][1]) > self.eps:
                                vis_relaLst[i] = 1
                                vis_ansrelaLst[j] = 1

                    if len(vis_relaLst):
                        P_i = sum(vis_relaLst) / len(vis_relaLst)
                        P.append(P_i)

                    if len(vis_ansrelaLst):
                        R_i = sum(vis_ansrelaLst)/len(vis_ansrelaLst)
                        R.append(R_i)
                    break

        P = 0 if len(P) == 0 else sum(P) / len(P)
        R = 0 if len(R) == 0 else sum(R) / len(R)
        print("[RESULT] 关系分析 Precision:{:.2f}".format(P))
        print("[RESULT] 关系分析 Recall:{:.2f}".format(R))
        return 0 if (P == 0 or R == 0) else 2 * P * R / (P + R)


if __name__ == '__main__':
    e = EvaluateOnCEC()
    e.evaluate()

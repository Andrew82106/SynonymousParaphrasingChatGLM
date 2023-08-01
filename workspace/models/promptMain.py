# -*- coding:UTF-8 -*-
import copy

from Utils.extractJson import extractJson, JsonValidate, JsonValidate_Detail
from Utils.GetRelationShips import GetRelationShips
from Utils.GetEventType import GetEventType
from Utils.GetEventDetail import GetEventDetail
from configs.pathcfg import Pcfg
# from Utils.load_model import chatglm
import json
import os
import sys
from Utils.debugformat import INFO, DEBUG, WARNING
sys.path.append(os.getcwd())


key = [['因果关系', '原因', '结果'], ['顺承关系', '前一事件', '后一事件']]


def ana_detail(relationJson, model, order):
    pos = 0
    detailJson = copy.deepcopy(relationJson)
    for item in detailJson[key[order][0]]:
        reason = item.split("->")[0]
        result = item.split("->")[1]
        reason_type = GetEventType(reason, model)
        result_type = GetEventType(result, model)
        detail1_raw = GetEventDetail(reason, reason_type, model)
        detail1 = extractJson(detail1_raw)
        detail2_raw = GetEventDetail(result, result_type, model)
        detail2 = extractJson(detail2_raw)
        if not JsonValidate_Detail(detail1) or not JsonValidate_Detail(detail2):
            WARNING(f"大模型分析{key[order][0]}有误")
            if not JsonValidate_Detail(detail1):
                DEBUG(f"detail1 raw:{detail1_raw}")
            if not JsonValidate_Detail(detail2):
                DEBUG(f"detail2 raw:{detail2_raw}")
            raise NotImplementedError
        detailJson[key[order][0]][pos] = {
            key[order][1]: {
                "事件类型": reason_type,
                "事件细节": json.loads(detail1),
                "事件描述": reason
            },
            key[order][2]: {
                "事件类型": result_type,
                "事件细节": json.loads(detail2),
                "事件描述": result
            }
        }
        pos += 1
    return detailJson


def detail(JsonIn: json, model):
    INFO("对事件进行归类和细节分析", level=0)
    # relationJson = json.loads(JsonIn)
    relationJson = JsonIn
    cntt = 1
    while cntt < Pcfg.maxReworkOfDetail:
        try:
            relationJson = ana_detail(relationJson, model, 0)
            INFO("尝试分析因果关系成功", level=0)
            break
        except Exception as e:
            INFO(f"尝试分析因果关系{cntt}/{Pcfg.maxReworkOfDetail}")
            cntt += 1
            continue
    cntt = 1
    flag1 = False if (cntt == Pcfg.maxReworkOfDetail) else True
    if not flag1:
        INFO("尝试分析因果关系失败", level=0)
        raise NotImplementedError
    while cntt < Pcfg.maxReworkOfDetail:
        try:
            relationJson = ana_detail(relationJson, model, 1)
            INFO("尝试分析顺承关系成功")
            break
        except Exception as e:
            INFO(f"尝试分析顺承关系{cntt}/{Pcfg.maxReworkOfDetail}")
            cntt += 1
            continue
    flag2 = False if (cntt == Pcfg.maxReworkOfDetail) else True
    if not flag2:
        INFO("尝试分析顺承关系失败", level=0)
    if flag1 and flag2:
        INFO("事件归类和细节分析成功", level=0)
    else:
        INFO("事件归类和细节分析失败", level=0)
    return relationJson


def process(Text, model):
    """
    调用该函数，获得对单个文本的分析结果
    """
    cnt = 0
    maxcnt = Pcfg.maxRework
    rawJson = -1
    while cnt < maxcnt:
        cnt += 1
        try:
            INFO(f"尝试对输入文本进行事件抽取({cnt}/{maxcnt}次)")
            relation = GetRelationShips(Text, model)
            DEBUG(f"relation from LLM:{relation}")
            # DEBUG(f"relationJson from LLM:{relationJson}")
            # relationJson = relationJson if JsonValidate(relationJson) else 'Json Invalidate'
            if not JsonValidate(relation):
                WARNING("大模型输出的json格式有误")
                continue
            else:
                relationJson = json.loads(relation)
                if len(relationJson['因果关系']) + len(relationJson['顺承关系']) != relation.count("->"):
                    WARNING("大模型输出的json格式有误")
                    continue
                INFO("成功得到事件关系json", level=0)
                rawJson = relationJson
            # relationJson = extractJson(relation)
            try:
                return detail(relationJson, model)
            except:
                WARNING("大模型事件细节分析有误")
                continue
        except Exception as e:
            WARNING(f"大模型输出的json格式有误:{e}")
            continue
    return rawJson


if __name__ == "__main__":
    text = "卢卡申科接着说：“热舒夫对他们来说是不可接受的。他们在阿尔捷莫夫斯克郊区作战时，他们知道（乌克兰的）军车来自哪里，他们由此印象深刻：热舒夫是我们的麻烦。当然，正如我们一致同意的，我把他们安顿在了白俄罗斯中部，我不想重新部署他们，因为他们现在精神有些低落……”"
    pass
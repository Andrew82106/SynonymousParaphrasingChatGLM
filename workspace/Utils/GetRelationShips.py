from load_model import chatglm
from Utils.debugformat import INFO, DEBUG, WARNING
from Utils.extractJson import extractJson, JsonValidate

background = """
我希望你能够以一名语言学家的身份完成我的任务。

我会给你一段文字，文字中有很多事件。

你需要做的事情是，首先提取出这些事件，然后提取出这些事件之间的因果关系和顺承关系，并且严格以json格式输出。

json只包含两个键，名为"顺承关系"和"因果关系"。

在表明事件之间的关系时，用且只用一个'->'符号来表示事件之间的因果或者顺承关系。
"""
Example1 = """
例子1：

文字：CryptoCore自2018年开始活跃，攻击了美国、以色列、欧洲和日本等国的加密货币交易所，造成的损失估计超过2亿美元。最初，ClearSky认为该团伙与乌克兰、俄罗斯和罗马尼亚等东欧国家有关。近期发现CryptoCore与F-Secure的活动高度一致，后者与Lazarus组织有关。研究人员还指出，黑客的活动也在扩大，最近开始将以色列作为目标。

输出：{}
""".format({"因果关系": ["CryptoCore的活跃活动->美国、以色列、欧洲和日本等国的加密货币交易所遭到攻击"], "顺承关系": ["ClearSky认为该团伙与乌克兰、俄罗斯和罗马尼亚等东欧国家有关->近期发现CryptoCore与F-Secure的活动高度一致"]})
Example2 = """
例子2：

文字：近日，DFIR研究人员检测到一起利用WebLogic远程代码执行漏洞(CVE-2020–14882)入侵并植入XMRig矿机的攻击活动。此次活动中，攻击者通过利用WebLogic漏洞入侵主机，执行PowerShell指令从远程服务器下载PowerShell脚本，获取后续组件加载XMRig。研究人员发现，攻击者利用netstat来查找是否有正在使用挖矿相关端口的进程，还禁用了防火墙规则以确保与矿池的稳定连接。

输出：{}
""".format({"因果关系": ["DFIR研究人员检测->攻击者的攻击活动", "攻击者利用WebLogic漏洞->攻击者入侵主机"], "顺承关系": ["攻击者利用WebLogic漏洞入侵主机->攻击者执行PowerShell指令从远程服务器下载PowerShell脚本", "攻击者执行PowerShell指令从远程服务器下载PowerShell脚本->获取后续组件加载XMRig"]})
Example3 = """
例子3：

文字：研究人员发现一项新的有针对性的网络钓鱼活动已将注意力集中在印度政府官员使用的名为Kavach的双因素身份验证上，根据与先前攻击的战术重叠，将其归因于名为 SideCopy 的威胁行为者。

输出：{}
""".format({"因果关系": ["研究人员发现->一项新的有针对性的网络钓鱼活动", "一项新的有针对性的网络钓鱼活动->将注意力集中在印度政府官员使用的身份验证上"], "顺承关系": ["研究人员发现->研究人员发将其归因于名为 SideCopy 的威胁行为者"]})
Example4 = """
例子4：

文字：12日早7时许， ２０８国道乌兰察布市察哈尔右翼后旗大陆号收费站北１．５公里处发生一起交通事故， 面包车内８名乘客全部死亡。 事故 原因是一辆银白色小面包车和一辆解放牌大货车相撞造成。 据死者家属介绍，他们是来自乌兰察布市兴和县二十号地村的村民， 欲前往察哈尔右翼前旗礼拜寺 做礼拜，车上共有３女５男。 他们乘坐的银灰色面包车由北向南 行驶， 与一辆货车相撞，车上８名乘客当即死亡。 验尸结束后， 尸体已经由家属认领 并作善后处理。 事故发生后，内蒙古交警总队及乌兰察布市交警支队工作人员赶到现场 对事故进行妥善处理。 事故原因正在进一步核查中。

输出：{}
""".format({"因果关系": ["与一辆货车相撞->８名乘客当即死亡"], "顺承关系": ["欲前往察哈尔右翼前旗礼拜寺->做礼拜", "验尸结束->尸体已经由家属认领", "事故发生->内蒙古交警总队及乌兰察布市交警支队工作人员赶到现场", "内蒙古交警总队及乌兰察布市交警支队工作人员赶到现场->对事故进行妥善处理"]})

Question1 = """
问题1：

文字：{}

输出：
"""


def GetRelationShips(text, model=None):
    prompt = background + Example1 + Example2 + Example3 + Example4 + Question1.format(text)
    if model is None:
        model = chatglm()
    # DEBUG(f"prompt:{prompt}")
    relation = model.response(prompt)[0].replace("\'", "\"")
    DEBUG(f"raw relation from LLM produce successfully")
    relationJson = extractJson(relation)
    DEBUG(f"relationJson from LLM:{relationJson}")
    relationJson = relationJson if JsonValidate(relationJson) else 'Json Invalidate'
    return relationJson


if __name__ == "__main__":
    text = "上周，包括乌克兰特勤局在内的三个乌克兰网络安全机构（乌克兰特勤局、 乌克兰网络警察和乌克兰CERT）警告称，与俄罗斯有关联的黑客针对其公共机构、地方政府进行了大规模鱼叉式网络钓鱼活动。6月初，攻击者伪装成政府机构发送了大量电子邮件，钓鱼邮件为税收主题，恶意附件为RAR格式，里面包含通过文件扩展名伪装的恶意exe文件。当运行这些文件时，将安装RemoteUtilities的修改版本，用于连接到攻击者的命令和控制服务器。目前，乌克兰安全局已公开了此次攻击的技术细节，如IoC、C2服务器和域名等，并建议相关组织对系统进行紧急检查，并及时采取预防措施。"
    print(GetRelationShips(text))

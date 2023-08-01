try:
    from load_model import chatglm
    from Utils.debugformat import INFO, DEBUG, WARNING
    from Utils.extractJson import extractJson, JsonValidate
except:
    from load_model import chatglm
    from debugformat import INFO, DEBUG, WARNING
    from extractJson import extractJson, JsonValidate

background = """
我会给你一段文字，你需要按照这段文字的逻辑将文字组成一个json并且输出
"""
Example1 = """
例子1：

文字：
>>>>
"攻击者"： "网络黑客"

"攻击手段"： "物理攻击"

输出：
>>>>
{}
""".format({"攻击者": "网络黑客", "攻击手段": "物理攻击"})
Example2 = """
例子2：

文字：近日，DFIR研究人员检测到一起利用WebLogic远程代码执行漏洞(CVE-2020–14882)入侵并植入XMRig矿机的攻击活动。此次活动中，攻击者通过利用WebLogic漏洞入侵主机，执行PowerShell指令从远程服务器下载PowerShell脚本，获取后续组件加载XMRig。研究人员发现，攻击者利用netstat来查找是否有正在使用挖矿相关端口的进程，还禁用了防火墙规则以确保与矿池的稳定连接。

输出：{}
""".format({"因果关系": ["DFIR研究人员检测->攻击者的攻击活动", "攻击者利用WebLogic漏洞->攻击者入侵主机"], "顺承关系": ["攻击者利用WebLogic漏洞入侵主机->攻击者执行PowerShell指令从远程服务器下载PowerShell脚本", "攻击者执行PowerShell指令从远程服务器下载PowerShell脚本->获取后续组件加载XMRig"]})
Example3 = """
例子3：

文字：研究人员发现一项新的有针对性的网络钓鱼活动已将注意力集中在印度政府官员使用的名为Kavach的双因素身份验证上，根据与先前攻击的战术重叠，将其归因于名为 SideCopy 的威胁行为者。

输出：{}
""".format({"因果关系": ["DFIR研究人员发现->一项新的有针对性的网络钓鱼活动", "一项新的有针对性的网络钓鱼活动->将注意力集中在印度政府官员使用的身份验证上"], "顺承关系": ["研究人员发现->研究人员发将其归因于名为 SideCopy 的威胁行为者"]})
Question1 = """
文字：
>>>>
{}

输出：
>>>>
"""

def wiseJson(text, model=None):
    prompt = background + Example1 + Question1.format(text)
    if model == None:
        model = chatglm()
    # DEBUG(f"prompt:{prompt}")
    jsonres = model.response(prompt)[0]
    jsonres = extractJson(jsonres).replace("\'", "\"")
    relationJson = jsonres if JsonValidate(jsonres) else 'Json Invalidate'
    return relationJson


if __name__ == "__main__":
    text = """
攻击者：通过在Steam平台上更新个人资料头像将恶意软件以加密的形式隐藏其中

攻击手段：利用Steam平台漏洞

攻击工具：未知

事件类型：攻击事件

    """
    print(wiseJson(text))
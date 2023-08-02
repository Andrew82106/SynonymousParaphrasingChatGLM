from Utils.loadTmodel import chatglm_ptuing


def getSimi(TextIn):
    model = chatglm_ptuing()
    return model.response(textIn=TextIn)[0]

print(getSimi("我今晚在酒店吃了一顿牛排"))

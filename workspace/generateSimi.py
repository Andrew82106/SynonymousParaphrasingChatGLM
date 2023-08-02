from Utils.loadTmodel import chatglm_ptuing
model = chatglm_ptuing()


def getSimi(TextIn):
    return model.response(textIn=TextIn)[0]


if __name__ == '__main__':
    print(getSimi("我今晚在酒店吃了一顿牛排"))


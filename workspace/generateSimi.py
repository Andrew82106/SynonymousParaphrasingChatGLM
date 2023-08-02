from Utils.loadTmodel import chatglm_ptuing

model = chatglm_ptuing()

print(model.response(textIn="我今晚在酒店吃了一顿牛排")[0])

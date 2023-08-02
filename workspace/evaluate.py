from Utils.loadTmodel import chatglm_ptuing
from paddlenlp import Taskflow
import tqdm

model = chatglm_ptuing()


def getSimi(TextIn):
    return model.response(textIn=TextIn)[0]


class Paddlesimilarity:
    def __init__(self):
        self.similarity = Taskflow("text_similarity")

    def likelyHood(self, text1, text2):
        return self.similarity([[text1, text2]])[0]['similarity']


def evaluate(InputTextList):
    resLst = []
    for i in tqdm.tqdm(InputTextList):
        resLst.append([i, getSimi(i)])
    x = Paddlesimilarity()
    print(x.likelyHood("我今晚在酒店吃了一顿牛排", "今晚我在酒店享用了一顿美味的牛排餐。"))
    simiRes = []
    for i in tqdm.tqdm(resLst):
        simiRes.append(x.likelyHood(i[0], i[1]))
    print(f"maxSimi={max(simiRes)} minSimi={min(simiRes)} avgSimi={sum(simiRes)/len(simiRes)}")


if __name__ == '__main__':
    with open("./qingbao.txt", "r", encoding='utf-8') as f:
        x = f.read()
        print(x)
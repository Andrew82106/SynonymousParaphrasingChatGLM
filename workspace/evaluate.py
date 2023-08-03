from Utils.loadTmodel import chatglm_ptuing
from paddlenlp import Taskflow
import tqdm

with open("./qingbao.txt", "r", encoding='utf-8') as f:
    x = f.read()
    lst = x.split("\n")
    print(len(lst))

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
        with open("./ResSimilarity.txt", 'w', encoding='utf-8') as f:
            f.write(str(resLst))
    x = Paddlesimilarity()
    simiRes = []
    cnt = 0
    for i in tqdm.tqdm(resLst):
        simiRes.append(x.likelyHood(i[0], i[1]))
        cnt += 1
        if cnt % 20 == 0:
            print(f"[Evaluate] average similarity at present is: {sum(simiRes)/len(simiRes)}")
        with open("./similarity.txt", 'w', encoding='utf-8') as f:
            f.write(str(simiRes))
    print(f"maxSimi={max(simiRes)} minSimi={min(simiRes)} avgSimi={sum(simiRes)/len(simiRes)}")


if __name__ == '__main__':
    evaluate(lst)

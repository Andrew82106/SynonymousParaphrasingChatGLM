from BaiduAPIsimilarity import BDsimilarity
from PaddleSimilarity import Paddlesimilarity
from OffLinesimilarity import OFFsimilarity


class Evaluate(Paddlesimilarity, OFFsimilarity, BDsimilarity):
    def __init__(self, baseDataset, rawRoute, cec, raw):
        super(Evaluate, self).__init__()
        self.baseDataset = baseDataset
        self.EvaluateDataset = rawRoute
        self.BaseJson = cec
        self.rawJson = raw
        self.newJson = None

    def evaluate(self):
        pass

    def formatData(self):
        pass


if __name__ == '__main__':
    e = Evaluate(None, None, None, None)
    txt1 = "理科不会了，鼓励娃一定多思考，哪怕能想到一步也行，做不出来答案也有收获"
    txt2 = "文科完全不一样，自己想往往瞎想，浪费时间"
    print(e.likelyHood(txt1, txt2))

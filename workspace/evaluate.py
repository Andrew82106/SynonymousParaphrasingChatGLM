from Utils.loadTmodel import chatglm_ptuing
from paddlenlp import Taskflow
import tqdm
import os
import json
import torch
from transformers import BertTokenizer, BertModel

with open("./qingbao.txt", "r", encoding='utf-8') as f:
    x = f.read()
    lst = x.split("\n")
    print(len(lst))


def getSimi(TextIn, model):
    return model.response(textIn=TextIn)[0]


class Paddlesimilarity:
    def __init__(self):
        self.similarity = Taskflow("text_similarity")

    def likelyHood(self, text1, text2):
        return self.similarity([[text1, text2]])[0]['similarity']


class Bertsimilarity:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')

    def likelyHood(self, text1, text2):
        # Tokenize and convert texts to model inputs
        inputs1 = self.tokenizer(text1, return_tensors="pt", padding=True, truncation=True)
        inputs2 = self.tokenizer(text2, return_tensors="pt", padding=True, truncation=True)

        # Get model outputs for both texts
        outputs1 = self.model(**inputs1)
        outputs2 = self.model(**inputs2)

        # Get embeddings of [CLS] token (representing the whole text)
        embeddings1 = outputs1.last_hidden_state[:, 0, :]
        embeddings2 = outputs2.last_hidden_state[:, 0, :]

        # Calculate cosine similarity between embeddings
        cosine_sim = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)

        return cosine_sim.item()


def evaluate(InputTextList):
    file_path = "./ResSimilarity.txt"

    if os.path.exists(file_path):
        # 文件存在，读取内容并转化为列表
        with open(file_path, 'r') as file:
            content = file.read()
            resLst = eval(content)
    else:
        model = chatglm_ptuing()
        resLst = []
        for i in tqdm.tqdm(InputTextList):
            resLst.append([i, getSimi(i, model)])
            with open("./ResSimilarity.txt", 'w', encoding='utf-8') as f:
                f.write(str(resLst))
    # x = Paddlesimilarity()
    x = Bertsimilarity()
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

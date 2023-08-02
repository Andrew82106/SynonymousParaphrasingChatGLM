from transformers import AutoTokenizer, AutoModel


class chatglm:
    def __init__(self):
        route = "../../THUDM/chatglm2-6b"
        self.tokenizer = AutoTokenizer.from_pretrained(route, trust_remote_code=True, revision="v1.0")
        self.model_0 = AutoModel.from_pretrained(route, trust_remote_code=True, device='cuda', revision="v1.0")
        self.model = self.model_0.eval()

    def response(self, textIn, history=None):
        try:
            if history is None:
                history = []
            res, history = self.model.chat(self.tokenizer, textIn, history=history)
            return res, history
        except Exception as e:
            return -1, e


if __name__ == "__main__":
    model = chatglm()
    res, history = model.response("我希望你能够以一名语言学家的身份完成我的任务。首先我会给你一段文字，你需要做的事情是，将我输入的文本按照你的理解复述成一段新的文本并且输出，保证信息完整不缺不漏。")
    print(res)
    res1, history = model.response("2018年6月，已在深圳打拼10年的梁文锦不想过一辈子打工人的生活，计划创业。他学工业设计，此前一直从事消费电子类产品的设计工作，还拥有两项设计相关的专利。", history=history)
    print(res1)
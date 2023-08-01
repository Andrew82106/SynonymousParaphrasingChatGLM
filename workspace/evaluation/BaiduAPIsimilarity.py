from aip import AipNlp
from similarity import similarity


class BDsimilarity(similarity):
    def __init__(self):
        super(BDsimilarity, self).__init__()
        self.APP_ID = '36764894'
        self.API_KEY = '4PP3IIXcbnE2fsTMt1ErQhfw'
        self.SECRET_KEY = 'teCnmsGhb2DhNzVG4ViNvYF0RrPpUszA'
        self.client = AipNlp(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def likelyHood(self, text1, text2):
        options = {}
        options["model"] = "CNN"
        try:
            return float(self.client.simnet(text1, text2, options)['score'])
        except Exception as e:
            print(self.client.simnet(text1, text2, options))
            raise e

from paddlenlp import Taskflow
from similarity import similarity


class Paddlesimilarity(similarity):
    def __init__(self):
        super(Paddlesimilarity, self).__init__()
        self.similarity = Taskflow("text_similarity")

    def likelyHood(self, text1, text2):

        return self.similarity([[text1, text2]])[0]['similarity']

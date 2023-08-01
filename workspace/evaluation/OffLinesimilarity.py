import re
import math
from similarity import similarity


class OFFsimilarity(similarity):
    def __init__(self):
        super(OFFsimilarity, self).__init__()

    @staticmethod
    def preprocess_text(text):
        # 去除标点符号
        text = re.sub(r'[^\w\s]', '', text)
        # 转换为小写
        text = text.lower()
        # 分词
        words = text.split()
        return words

    @staticmethod
    def compute_word_frequency(words):
        word_frequency = {}
        for word in words:
            word_frequency[word] = word_frequency.get(word, 0) + 1
        return word_frequency

    def compute_cosine_similarity(self, text1, text2):

        words1 = self.preprocess_text(text1)
        words2 = self.preprocess_text(text2)

        word_frequency1 = self.compute_word_frequency(words1)
        word_frequency2 = self.compute_word_frequency(words2)

        intersection = set(word_frequency1.keys()) & set(word_frequency2.keys())
        dot_product = sum(word_frequency1[word] * word_frequency2[word] for word in intersection)

        magnitude1 = math.sqrt(sum(word_frequency1[word] ** 2 for word in words1))
        magnitude2 = math.sqrt(sum(word_frequency2[word] ** 2 for word in words2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        else:
            return dot_product / (magnitude1 * magnitude2)

    def likelyHood(self, text1, text2):
        return self.compute_cosine_similarity(text1, text2)

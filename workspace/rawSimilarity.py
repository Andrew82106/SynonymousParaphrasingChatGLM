import torch
from transformers import BertTokenizer, BertModel

def bert_text_similarity(text1, text2):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Tokenize and convert texts to model inputs
    inputs1 = tokenizer(text1, return_tensors="pt", padding=True, truncation=True)
    inputs2 = tokenizer(text2, return_tensors="pt", padding=True, truncation=True)

    # Get model outputs for both texts
    outputs1 = model(**inputs1)
    outputs2 = model(**inputs2)

    # Get embeddings of [CLS] token (representing the whole text)
    embeddings1 = outputs1.last_hidden_state[:, 0, :]
    embeddings2 = outputs2.last_hidden_state[:, 0, :]

    # Calculate cosine similarity between embeddings
    cosine_sim = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)

    return cosine_sim.item()

text1 = "BlueNoroff(也被称为APT38)是一个出于经济动机的APT组织，也是臭名昭著的Lazarus Group的一个下属组织。据观察，该团伙近期采用了能够绕过Windows Mark of the Web(MotW)保护的新技术。BlueNoroff通常利用Word文档和快捷方式文件进行初步入侵。但由于当用户试图打开从互联网下载的Microsoft Office文件时，操作系统会在受保护的视图中打开它，这会限制嵌入式宏的执行(即Windows MotW保护)。为此，该组织最近采用了旨在规避MOTW的新方法：即利用光盘映像(.iso 扩展名）和虚拟硬盘(.vhd扩展名）文件形式传播恶意软件。此外，BlueNoroff还创建了大量冒充风险投资公司和银行的虚假域名，一些虚假域名被发现模仿ABF Capital、Angel Bridge、ANOBAKA、美国银行和三菱UFJ金融集团，但其中大部分域名位于日本。05SideCopy针对印度政府官员进行网络攻"
text2 = "BlueNoroff，即APT38，是一个由经济动机驱动的APT组织，同时也是臭名昭著的Lazarus Group的下属组织。最近，该团伙开始采用新技术，绕过了Windows Mark of the Web（MotW）保护，通过使用光盘映像（.iso 扩展名）和虚拟硬盘（.vhd 扩展名）文件来传播恶意软件。此外，BlueNoroff还创建了大量的虚假域名，试图模仿ABF Capital、Angel Bridge、ANOBAKA、美国银行和三菱UFJ金融集团，但大部分域名都位于日本。最近，印度政府官员成为了网络攻击的目标。"

similarity_score = bert_text_similarity("423554235654375345252637356为3", "BlueNoroff(也被称为APT38)是一个出于经济动机的APT组织")
print(f"BERT Text Similarity Score: {similarity_score}")
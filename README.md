# LLM_NER

## introduction

本项目使用提示工程，经过多轮询问得到输入文本的事件关系

![WechatIMG976.jpg](src/WechatIMG976.jpg)

## usage

### 环境配置

首先需要下载本仓库：

```shell
git clone https://github.com/Andrew82106/LLM_NER.git
cd LLM_NER
```

然后使用 pip 安装依赖：

```
pip install -r requirements.txt
```

其中 `transformers` 库版本推荐为 `4.30.2`，`torch` 推荐使用 2.0 及以上的版本，以获得最佳的推理性能。

本项目默认使用ChatGLM2-6B模型，因此此时下ChatGLM2-6B模型权重文件

从 Hugging Face Hub 下载模型需要先[安装Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)，然后运行

```Shell
git clone https://huggingface.co/THUDM/chatglm2-6b
```

如果你从 Hugging Face Hub 上下载 checkpoint 的速度较慢，可以只下载模型实现

```Shell
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/THUDM/chatglm2-6b
```

将下载好的模型实现（chatglm2-6b文件夹）中的内容放到本项目的``THUDM/chatglm2-6b``文件夹下

然后从[这里](https://cloud.tsinghua.edu.cn/d/674208019e314311ab5c/)手动下载模型参数文件，并将下载的文件替换到本项目的``THUDM/chatglm2-6b``文件夹下

### 单文本处理

将文本放到项目``ChatGLM2-6B/workspace/input/single.txt``中，然后运行：

`` python main.py --task single --savepath ./single_ana_res.json``

即可在文件``single_ana_res.json``中找到处理结果

### 文本批量处理

将文本放到项目``ChatGLM2-6B/workspace/input/batches.txt``中，以换行分割样本，然后运行：

`` python main.py --task batches --savepath ./batches_ana_res.json``

即可在文件``batches_ana_res.json``中找到处理结果

## evaluate

本项目使用CEC数据集对效果进行评测([repo link](https://github.com/shijiebei2009/CEC-Corpus))

评测方法的实现在evaluation文件夹下

其中事件抽取评测结果如下：

|关注的样本事件关系类型|相似度阈值|合法样本占比|Precision|Recall|F1|
|--|--|--|--|--|--|
|['All Type']|0.7|78.68%|0.82|0.35|0.49|
|['Causal', 'Follow', 'Accompany']|0.7|78.68%|0.69|0.45|0.54|
|['Causal', 'Follow']|0.7|78.68%|0.54|0.44|0.48|
|['Causal', 'Accompany']|0.7|78.68%|0.51|0.47|0.49|
|['Follow', 'Accompany']|0.7|78.68%|0.52|0.40|0.45|
|['Accompany']|0.7|78.68%|0.27|0.42|0.33|
|['Follow']|0.7|78.68%|0.41|0.25|0.31|
|['Causal']|0.7|78.68%|0.30|0.40|0.34|
|['Causal']|0.65|78.68%|0.34|0.44|0.38|
|['Causal']|0.6|78.68%|0.39|0.49|0.44|


(向大模型中输入的样本可能会出现无法输出合法分析结果的情况，我们将能够合法输出分析结果的样本叫做合法样本)

关系抽取评测结果如下：

|关注的样本事件关系类型|相似度阈值|合法样本占比|Precision|Recall|F1|
|--|--|--|--|--|--|
|['Causal']|0.6|78.68%|0.58|0.77|0.67|
|['Causal']|0.65|78.68%|0.46|0.46|0.46|
|['Causal']|0.7|78.68%|0.28|0.21|0.24|
|['Follow']|0.7|78.68%|0.23|0.16|0.19|
|['Causal', 'Follow']|0.7|78.68%|0.44|0.35|0.39|

## ChatGLM2-6B

本项目基于ChatGLM2-6B([repo link](https://github.com/THUDM/ChatGLM2-6B))进行开发，主要代码在``workspace``文件下

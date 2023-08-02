# Synonymous Paraphrasing ChatGLM

## introduction

基于微调实现同义转述的chatGLM

实现效果为，对于一段输入的文本，输出文本为对输入文本的复述，复述相似度达到70%以上

## usage

首先根据chatGLM的配置方式配置好chatGLM模型

## ptuning data

in file ``SynonymousParaphrasing.json``

### how to get data for ptuning?

use the prompt to GPT3:

``用中文给我生成一句话，长度大于70字，然后为这句话生成19句同义句，然后将这20句话放在一个python列表里面输出``

repeat it and you will get enough data
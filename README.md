# Synonymous Paraphrasing ChatGLM

## introduction

基于微调实现同义转述的chatGLM

实现效果为，对于一段输入的文本，输出文本为对输入文本的复述

## usage

本项目默认使用ChatGLM2-6B模型，因此此时下载ChatGLM2-6B模型权重文件

从 Hugging Face Hub 下载模型需要先[安装Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)，然后运行

``git clone https://huggingface.co/THUDM/chatglm2-6b``

如果你从 Hugging Face Hub 上下载 checkpoint 的速度较慢，可以只下载模型实现

``GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/THUDM/chatglm2-6b``

将下载好的模型实现（chatglm2-6b文件夹）中的内容放到本项目的``workspace/THUDM/chatglm2-6b``文件夹下

然后从这里手动下载模型参数文件，并将下载的文件替换到本项目的``workspace/THUDM/chatglm2-6b``文件夹下


## ptuning

### ptuning data

在文件``workspace/SynonymousParaphrasing.json``中

#### how to get data for ptuning?

对chatGPT3使用如下提示词:

``用中文给我生成一句话，长度大于70字，然后为这句话生成19句同义句，然后将这20句话放在一个python列表里面输出``

不断地重复就可以得到足够的训练数据

### ptuning process

首先根据chatGLM的配置方式配置好chatGLM模型([repo link](https://github.com/THUDM/ChatGLM2-6B))

按照chatGLM模型的readme指导，调整``ptuning``文件夹下的``train.sh``中的部分行，如下所示：

```shell
    --train_file SynonymousParaphrasingDataset/train.json \
    --validation_file SynonymousParaphrasingDataset/test.json \
    ......
    --prompt_column input \
    --response_column output \
    ......
```

然后运行命令``bash train.sh``即可。

## evaluate

- demo:

```text
input: 'CNC组织最早于2019年被发现，其命名来源于所使用的远控木马的PDB路径信息中包含的cnc_client，且该组织主要针对军工和教育行业进行攻击。近期，研究人员披露了该组织所使用的两个下载器：PrivateImage.png.exe和YodaoCloudMgr.exe。PrivateImage.png.exe下载器具有摆渡攻击的能力，可利用移动存储设备作为“渡船”，间接从隔离网中窃取攻击者感兴趣的文件。即PrivateImage.png.exe会根据是否在%localappdata%路径下选择两种方式执行。若在%localappdata%路径下，其将不断检测是否有新设备接入；若有，则将文件本身复制到新设备中，以便通过可移动设备传播。反之，首先判断%localappdata%\\ImageEditor.exe是否存在：若存在，跳过后续操作并退出。不存在，判断互联网连接状态：若可连网，便下载YodaoCloudMgr.exe下载器。YodaoCloudMgr.exe主要用于下载后续载荷，且该下载器使用欺骗性的具有不可信数字证书的C2节点进行通信。

output:'2019年，一家名为CNC的组织被发现使用远控木马攻击了军工和教育行业，该组织的命名来源于使用的远控木马PDB路径中的cnc_client，主要针对军工和教育行业进行攻击。最近，研究人员透露了该组织使用的两个下载器：PrivateImage.png.exe和YodaoCloudMgr.exe。PrivateImage.png.exe可以利用移动存储设备作为“渡船”，通过隔离网从攻击者手中窃取感兴趣的文件。即PrivateImage.png.exe将在%localappdata%路径下，根据是否在%localappdata%路径下选择两种方式执行：若在%localappdata%路径下，其将不断检测是否有新设备接入；若有，则将文件本身复制到新设备中，以便通过可移动设备传播。反之，首先判断%localappdata%\\ImageEditor.exe是否存在：若存在，跳过后续操作并退出。如果不存在，将判断互联网连接状态：若可连网，便下载YodaoCloudMgr.exe下载器。YodaoCloudMgr.exe主要用于下载后续载荷，且该下载器使用欺骗性的具有不可信数字证书的C2节点进行通信。
```
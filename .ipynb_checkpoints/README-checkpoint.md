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
input: 

CNC组织最早于2019年被发现，其命名来源于所使用的远控木马的PDB路径信息中包含的cnc_client，且该组织主要针对军工和教育行业进行攻击。
近期，研究人员披露了该组织所使用的两个下载器：PrivateImage.png.exe和YodaoCloudMgr.exe。PrivateImage.png.exe下载器具有摆渡攻击的能力，可利用移动存储设备作为“渡船”，间接从隔离网中窃取攻击者感兴趣的文件。
即PrivateImage.png.exe会根据是否在%localappdata%路径下选择两种方式执行。若在%localappdata%路径下，其将不断检测是否有新设备接入；若有，则将文件本身复制到新设备中，以便通过可移动设备传播。反之，首先判断%localappdata%\\ImageEditor.exe是否存在：若存在，跳过后续操作并退出。不存在，判断互联网连接状态：若可连网，便下载YodaoCloudMgr.exe下载器。
YodaoCloudMgr.exe主要用于下载后续载荷，且该下载器使用欺骗性的具有不可信数字证书的C2节点进行通信。

output:

2019年，一家名为CNC的组织被发现使用远控木马攻击了军工和教育行业，该组织的命名来源于使用的远控木马PDB路径中的cnc_client，主要针对军工和教育行业进行攻击。
最近，研究人员透露了该组织使用的两个下载器：PrivateImage.png.exe和YodaoCloudMgr.exe。PrivateImage.png.exe可以利用移动存储设备作为“渡船”，通过隔离网从攻击者手中窃取感兴趣的文件。
即PrivateImage.png.exe将在%localappdata%路径下，根据是否在%localappdata%路径下选择两种方式执行：若在%localappdata%路径下，其将不断检测是否有新设备接入；若有，则将文件本身复制到新设备中，以便通过可移动设备传播。反之，首先判断%localappdata%\\ImageEditor.exe是否存在：若存在，跳过后续操作并退出。如果不存在，将判断互联网连接状态：若可连网，便下载YodaoCloudMgr.exe下载器。
YodaoCloudMgr.exe主要用于下载后续载荷，且该下载器使用欺骗性的具有不可信数字证书的C2节点进行通信。
```

```text
input:

BlueNoroff(也被称为APT38)是一个出于经济动机的APT组织，也是臭名昭著的Lazarus Group的一个下属组织。
据观察，该团伙近期采用了能够绕过Windows Mark of the Web(MotW)保护的新技术。BlueNoroff通常利用Word文档和快捷方式文件进行初步入侵。
但由于当用户试图打开从互联网下载的Microsoft Office文件时，操作系统会在受保护的视图中打开它，这会限制嵌入式宏的执行(即Windows MotW保护)。
为此，该组织最近采用了旨在规避MOTW的新方法：即利用光盘映像(.iso 扩展名）和虚拟硬盘(.vhd扩展名）文件形式传播恶意软件。
此外，BlueNoroff还创建了大量冒充风险投资公司和银行的虚假域名，一些虚假域名被发现模仿ABF Capital、Angel Bridge、ANOBAKA、美国银行和三菱UFJ金融集团，但其中大部分域名位于日本。
05SideCopy针对印度政府官员进行网络攻

output:

BlueNoroff，即APT38，是一个由经济动机驱动的APT组织，同时也是臭名昭著的Lazarus Group的下属组织。
最近，该团伙开始采用新技术，绕过了Windows Mark of the Web（MotW）保护，通过使用光盘映像（.iso 扩展名）和虚拟硬盘（.vhd 扩展名）文件来传播恶意软件。
此外，BlueNoroff还创建了大量的虚假域名，试图模仿ABF Capital、Angel Bridge、ANOBAKA、美国银行和三菱UFJ金融集团，但大部分域名都位于日本。
最近，印度政府官员成为了网络攻击的目标。
```
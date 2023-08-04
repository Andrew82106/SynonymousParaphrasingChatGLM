import matplotlib.pyplot as plt
import pprint
import pandas as pd
with open("./similarity.txt", "r", encoding='utf-8') as f:
    a = f.read()
    data_list = eval(str(a))


def plot_list_distribution(data_list):
    algo = "paddle"
    # 创建一个直方图
    plt.hist(data_list, bins=20, edgecolor='black')

    # 添加标签和标题
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of content similarity in the List(using {algo} similarity)')

    # 显示图形

    plt.savefig(f"simi_{algo}.png")

    plt.show()


# 绘制分布图
plot_list_distribution(data_list)


def getSample():
    dicc = {"original content": [], "content": []}
    file_path = "./ResSimilarity.txt"
    
    with open(file_path, 'r') as file:
        content = file.read()
        resLst = eval(content)

    cnt = 0
    for i in data_list:
        if i < -0.4:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nscore:{}\ncontent:{}\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>".format(data_list[cnt], resLst[cnt]))
        cnt += 1
        if cnt > 100:
            break
    for i in resLst:
        dicc['content'].append(i[1])
        dicc['original content'].append(i[0])
    df = pd.DataFrame(dicc)
    df.to_csv("./enhanced.csv")

getSample()
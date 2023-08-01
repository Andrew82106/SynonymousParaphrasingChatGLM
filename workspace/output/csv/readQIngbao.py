import pandas as pd

df = pd.read_csv("./qingbao.csv", on_bad_lines='skip')

res = []

for i in df['content']:
    res.append(i.replace("\n", ""))

with open("./qingbao.txt", "w", encoding='utf-8') as f:
    for i in res:
        f.write(i+"\n")

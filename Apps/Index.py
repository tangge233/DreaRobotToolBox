import os
import json

json_data = []

print("Start runing...")

for filename in os.listdir():
    #print("Current file:",filename)
    if filename.endswith('.json') and filename != 'Index.json':
        with open(filename,"r",encoding="utf-8") as AppInfo:
            data = json.load(AppInfo)
            ThisAppInfo={
                "Name" : data['Name'],
                "Version" : data['Version'],
                "Author" : {
                    "Name" : data['Author']['Name'],
                    "HomePage" : data['Author']['HomePage']
                },
                "HomePage" : data['HomePage']
            }
            #print(ThisAppInfo)
            json_data.append(ThisAppInfo)

# 将所有数据写入 result.json 文件中
with open('Index.json', 'w',encoding="utf-8") as f:
    json.dump(json_data, f,ensure_ascii = False)

print("Operation end")
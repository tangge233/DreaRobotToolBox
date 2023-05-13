import os
import json

json_data = []


print("Start preparing the Index file")

for filename in os.listdir("Apps"):
    #print("Current file:",filename)
    if filename.endswith('.json') and filename != 'Index.json':
        with open("Apps/" + filename,"r",encoding="utf-8") as AppInfo:
            data = json.load(AppInfo)
            ThisAppInfo={
                "Name" : data['Name'],
                "Version" : data['Version'],
                "Author" : {
                    "Name" : data['Author']['Name'],
                    "HomePage" : data['Author']['HomePage']
                },
                "Desc" : data['Desc'],
                "HomePage" : data['HomePage']
            }
            #print(ThisAppInfo)
            json_data.append(ThisAppInfo)

# 将所有数据写入 result.json 文件中
with open('Apps/Index.json', 'w',encoding="utf-8") as f:
    json.dump(json_data, f,ensure_ascii = False)

print("Index file preparation completed")
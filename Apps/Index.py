import os
import json

json_data = []

def DecodeSize(size):
    unit = ["","K","M","G","T","P"] #No application will be so huge,right?
    res = size
    i = 0
    while res > 1024:
        res = res / 1024
        i+=1
    if i + 1 > len(unit):
        i = 0
        res = size
    res = round(res,2)
    return str(res) + " " + unit[i] + "B"


print("Start preparing the Index file")

for filename in os.listdir("Apps"):
    #print("Current file:",filename)
    if filename.endswith('.json') and filename != 'Index.json':
        print("Record",filename,"into Index file.")
        with open("Apps/" + filename,"r",encoding="utf-8") as AppInfo:
            data = json.load(AppInfo)
            ThisAppInfo={
                "Name" : data['Name'],
                "Version" : data['Version'],
                "Author" : {
                    "Name" : data['Author']['Name'],
                    "HomePage" : data['Author']['HomePage']
                },
                "Size" : DecodeSize(os.path.getsize("Apps/" + os.path.splitext(filename)[0] + ".dll")),
                "Desc" : data['Desc'],
                "HomePage" : data['HomePage']
            }
            #print(ThisAppInfo)
            json_data.append(ThisAppInfo)

# 将所有数据写入 result.json 文件中
with open('Apps/Index.json', 'w',encoding="utf-8") as f:
    json.dump(json_data, f,ensure_ascii = False)

print("Index file preparation completed")
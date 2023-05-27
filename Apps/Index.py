import os
import json
import hashlib
import requests
import urllib
  
def Calculate_sha256(file_path):  
    sha256 = hashlib.sha256()  
    with open(file_path, 'rb') as f:  
        while True:  
            data = f.read(1024)  
            if not data:  
                break  
            sha256.update(data)  
    return sha256.hexdigest()  

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

json_data = []

for filename in os.listdir("Apps"):
    #print("Current file:",filename)
    if filename.endswith('.json') and filename != 'Index.json':
        ThisAppID = os.path.splitext(filename)[0]
        ThisJsonFile = "Apps/" + filename
        ThisAppFile = "Apps/" + ThisAppID + ".dll"
        print(ThisAppID,":Record into Index file.")
        print(ThisAppID,":Json file name:",filename)
        if not os.path.exists(ThisAppFile):
            print(ThisAppID,":Application not exists,deleting its json file")
            os.remove(ThisJsonFile)
            continue
        with open("Apps/" + filename,"r",encoding="utf-8") as AppInfo:
            data = json.load(AppInfo)
            ThisAppSHA = Calculate_sha256(ThisAppFile)
            ThisAppVersion = data['Version']
            ThisAppDesc = data['Desc']
            if "UpdateInfo" in data:
                print(ThisAppID,":Try to get remote infomation")
                try:
                    ThisAppRemoteInfo = requests.get(data['Update'],timeout=20).json
                    if "SHA256" in ThisAppRemoteInfo and "Version" in ThisAppRemoteInfo and "Desc" in ThisAppRemoteInfo and "Download" in ThisAppRemoteInfo:
                        if ThisAppRemoteInfo['SHA256'] != ThisAppSHA:
                            print(ThisAppID,":Find update")
                            NewAppFile = "Apps/" + ThisAppID + "_new.dll"
                            with urllib.request.urlopen(ThisAppRemoteInfo['Download']) as response, open(NewAppFile, 'wb') as out_file:  
                                out_file.write(response.read())
                                print(ThisAppID,":Donwload complete")
                                NewFileSHA = Calculate_sha256("Apps/" + ThisAppID + "_new.dll")
                                if NewFileSHA == ThisAppRemoteInfo['SHA256']:
                                    print(ThisAppID,":Upgrade pass check")
                                    ThisAppSHA = NewFileSHA
                                    ThisAppVersion = ThisAppRemoteInfo['Version']
                                    ThisAppDesc = ThisAppRemoteInfo['Desc']

                                    os.remove(ThisAppFile)
                                    os.rename(NewAppFile,ThisAppFile)
                                    print(ThisAppID,":Upgrade success!")
                                else:
                                    os.remove(NewAppFile)
                                    print(ThisAppID,":Remote file sha256 is not correct!")
                            # Won't update the infomation of this app if fail
                            
                except:
                    pass

            ThisAppInfo={
                "Name" : data['Name'],
                "ID" : ThisAppID,
                "Version" : ThisAppVersion,
                "Author" : {
                    "Name" : data['Author']['Name'],
                    "HomePage" : data['Author']['HomePage']
                },
                "Size" : DecodeSize(os.path.getsize("Apps/" + ThisAppID + ".dll")),
                "SHA256" : ThisAppSHA,
                "Desc" : ThisAppDesc,
                "HomePage" : data['HomePage']
            }
            #print(ThisAppInfo)
            json_data.append(ThisAppInfo)

# 将所有数据写入 result.json 文件中
with open('Apps/Index.json', 'w',encoding="utf-8") as f:
    json.dump(json_data, f,ensure_ascii = False)

print("Index file preparation completed")
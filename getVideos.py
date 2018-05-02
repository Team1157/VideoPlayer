import subprocess, re, os
with open('Videos.txt', 'r') as f:
    global VideoList
    global newVideoList
    VideoList = f.readlines()
    newVideoList = []
    for item in VideoList:
        item = item.replace("\n", "")
        newVideoList.append(item)
if newVideoList:
    for Video in newVideoList:
        name = re.findall(r".*\/(.*)", Video)[0]
        if not name in os.listdir("Videos"):
            subprocess.call("cd Videos && wget %s" % Video, shell=True)
        else:
            print("File does exist")

import zipfile
import os

gameList = []


# 获取zip
def ZipPath(pathname):
    for path, directory, files in os.walk(pathname):
        for file in files:
            if file.split('.')[-1] != 'zip':
                break
            else:
                return path, directory, file


def filepath(pathname):
    for path, directory, files in os.walk(pathname):
        for file in files:
            return gameList.append(file)


# 解压zip
p, d, f = ZipPath('../res/')
print(str(f).split('.')[0])
Zfile = zipfile.ZipFile((str(p) + str(f)), 'r')
for filename in Zfile.namelist():
    Zfile.extract(filename, str(p))
Zfile.close()

# 获取大厅u3d图片
gamepath = '../res/' + str(f).split('.')[0] + 'phone/prefabs/game'
print(gamepath)
f2 = filepath(gamepath)
print(f2)

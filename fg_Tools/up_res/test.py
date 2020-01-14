import os
import re


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# print(is_number('jjhall_217'))
# print(is_number('123'))

def is_dis():
    if os.path.exists('up_res2.0.py'):
        return True
    else:
        return False


def find_xml(path):
    file = open(path, 'rb')
    for line in file.readlines():
        if line.decode('utf-8').find('<LobbyHallVersion>') == -1:
            continue
        else:
            return re.findall(r"\d+", line.decode('utf-8'))


# version = find_xml('../Phone/AssetBundle/Android5.0/jjhall_217/version_1.xml')
# if version is not None:
#     version = int(version[0]) + 1
#     version = 'version_' + str(version)
#     print(version)
# else:
#     print('not found')


name = '12000'
if name.isdecimal():
    print('True')
else:
    print('False')

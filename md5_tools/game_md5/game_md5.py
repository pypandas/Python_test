# -*- coding: utf-8 -*-
import os
import hashlib
import xml.etree.ElementTree as ET


def xmlchangemd5(xmlpath):
    tree = ET.ElementTree()
    tree.parse(xmlpath)
    temp = tree.getroot()
    luamd5 = md5('lua.zip')
    resmd5 = md5('resources.zip')
    luavesion = int(temp.find('LobbyLuaVersion').text)
    resvesion = int(temp.find('LobbyResVersion').text)
    if alter(xmlpath, str(temp.find('LobbyLuaMD5').text), luamd5):
        alter(xmlpath, '<LobbyLuaVersion>' + str(luavesion),
              '<LobbyLuaVersion>' + str(luavesion + 1))
    if alter(xmlpath, str(temp.find('LobbyResMD5').text), resmd5):
        alter(xmlpath, '<LobbyResVersion>' + str(resvesion),
              '<LobbyResVersion>' + str(resvesion + 1))


def md5(name):
    namepath = os.path.join('./', name)
    fp = open(namepath, 'rb')
    contents = fp.read()
    fp.close()
    filemd5 = hashlib.md5(contents).hexdigest()
    return filemd5


def alter(file, old_str, new_str):
    if old_str != new_str:
        a = open(file, 'rb')
        str1 = a.read().decode('utf-8')
        str1 = str1.replace(old_str, new_str)
        b = open(file, 'wb')
        b.write(str1.encode('utf-8'))
        b.close()
        return 1
    else:
        return 0


if __name__ == '__main__':
    files = os.listdir('./')
    for i in files:
        if str(i).split('.')[-1] == 'xml':
            xmlpath = os.path.join('./', i)
            xmlchangemd5(xmlpath)

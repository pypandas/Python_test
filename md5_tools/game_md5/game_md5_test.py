# -*- coding: utf-8 -*-
import hashlib
import os
import xml.etree.ElementTree as ET


def find_zip_file(zip_path):
    zip_file_list = []
    file_list = os.listdir(zip_path)
    for zip_file in file_list:
        if os.path.isdir(zip_file):
            continue
        elif str(zip_file).split('.')[-1] != 'zip':
            continue
        else:
            zip_file_list.append(zip_file)
    return zip_file_list


def md5(file_md5, zip_path):
    name_path = os.path.join(zip_path, file_md5)
    fp = open(name_path, 'rb')
    contents = fp.read()
    fp.close()
    zip_md5 = hashlib.md5(contents).hexdigest()
    return zip_md5


def parse_xml(xml_file, zip_path):
    version_dict = {}
    tree = ET.ElementTree()
    tree.parse(str(xml_file))
    temp = tree.getroot()
    lua_version = int(temp.find('LobbyLuaVersion').text)
    res_version = int(temp.find('LobbyResVersion').text)
    try:
        lua_md5 = temp.find('LobbyLuaMD5').text
    except AttributeError:
        lua_md5 = 'add'
    try:
        res_md5 = temp.find('LobbyResMD5').text
    except AttributeError:
        res_md5 = 'add'
    for file_md5 in find_zip_file(zip_path):
        if file_md5 == 'lua.zip':
            if lua_md5 != md5(file_md5, zip_path):
                version_dict['LobbyLuaMD5'] = md5(file_md5, zip_path)
                if lua_version != 0:
                    version_dict['LobbyLuaVersion'] = lua_version + 1
                else:
                    version_dict['LobbyLuaVersion'] = lua_version
            else:
                version_dict['LobbyLuaMD5'] = lua_md5
                version_dict['LobbyLuaVersion'] = lua_version
        elif file_md5 == 'resources.zip':
            if res_md5 != md5(file_md5, zip_path):
                version_dict['LobbyResMD5'] = md5(file_md5, zip_path)
                version_dict['LobbyResVersion'] = res_version + 1
            else:
                version_dict['LobbyResMD5'] = res_md5
                version_dict['LobbyResVersion'] = res_version
        else:
            continue
    return version_dict


def write_version(ver_dict, file):
    ver_file_write = open(file, 'wb')
    ver_file_write.write(b'<?xml version="1.0"?>\r\n')
    ver_file_write.write(b'<ROOT>\r\n')
    ver_file_write.write(
        ('  <LobbyResVersion>' + str(ver_dict['LobbyResVersion']) + '</LobbyResVersion>\r\n').encode('utf-8'))
    ver_file_write.write(
        ('  <LobbyLuaVersion>' + str(ver_dict['LobbyLuaVersion']) + '</LobbyLuaVersion>\r\n').encode('utf-8'))
    ver_file_write.write(
        ('  <LobbyResMD5>' + str(ver_dict['LobbyResMD5']) + '</LobbyResMD5>\r\n').encode('utf-8')
    )
    ver_file_write.write(
        ('  <LobbyLuaMD5>' + str(ver_dict['LobbyLuaMD5']) + '</LobbyLuaMD5>\r\n').encode('utf-8')
    )
    ver_file_write.write(b'</ROOT>')
    ver_file_write.close()


if __name__ == '__main__':

    # 获取version.xml
    for _dir, _root, _file in os.walk('.\\'):
        v = [f for f in _file if f == 'version.xml']
        if len(v) == 0:
            continue
        else:
            ver_xml = os.path.join(_dir, v[0])
            response = parse_xml(ver_xml, _dir)
            print(response)
            # write_version(response, ver_xml)

# -*- coding: utf-8 -*-
import hashlib
import os
import xml.etree.ElementTree as ET


def find_zip_file():
    zip_file_list = []
    file_list = os.listdir('./')
    for zip_file in file_list:
        if os.path.isdir(zip_file):
            continue
        elif str(zip_file).split('.')[-1] != 'zip':
            continue
        else:
            zip_file_list.append(zip_file)
    return zip_file_list


def md5(file_md5):
    name_path = os.path.join('./', file_md5)
    fp = open(name_path, 'rb')
    contents = fp.read()
    fp.close()
    zip_md5 = hashlib.md5(contents).hexdigest()
    return zip_md5


def parse_xml(xml_file):
    version_dict = {'lua': {}, 'res': {}}
    tree = ET.ElementTree()
    tree.parse(str(xml_file))
    temp = tree.getroot()
    lua_version = int(temp.find('LobbyLuaVersion').text)
    res_version = int(temp.find('LobbyResVersion').text)
    lua_md5 = temp.find('LobbyLuaMD5').text
    res_md5 = temp.find('LobbyResMD5').text
    for file_md5 in find_zip_file():
        if file_md5 == 'lua.zip':
            if lua_md5 != md5(file_md5):
                version_dict['lua']['old_LobbyLuaMD5'] = lua_md5
                version_dict['lua']['LobbyLuaMD5'] = md5(file_md5)
                version_dict['lua']['old_LobbyLuaVersion'] = lua_version
                if lua_version != 0:
                    version_dict['lua']['LobbyLuaVersion'] = lua_version + 1
                else:
                    version_dict['lua']['LobbyLuaVersion'] = lua_version
            else:
                continue
        elif file_md5 == 'resources.zip':
            if res_md5 != md5(file_md5):
                version_dict['res']['old_LobbyResMD5'] = res_md5
                version_dict['res']['LobbyResMD5'] = md5(file_md5)
                version_dict['res']['old_LobbyResVersion'] = res_version
                version_dict['res']['LobbyResVersion'] = res_version + 1
            else:
                continue
        else:
            continue
    return version_dict


def write_version(ver_dict, file):
    version_file_read = open(file, 'rb')
    dumps = version_file_read.read().decode('utf-8')

    if ver_dict['res'] is not None:
        old_res_md5 = ver_dict['res']['old_LobbyResMD5']
        res_md5 = ver_dict['res']['LobbyResMD5']
        old_res_ver = ver_dict['res']['old_LobbyResVersion']
        res_ver = ver_dict['res']['LobbyResVersion']
        sed_res_md5 = dumps.replace(old_res_md5, res_md5)
        sed_res_ver = dumps.replace('<LobbyResVersion>' + str(old_res_ver), '<LobbyResVersion>' + str(res_ver))
        version_file_write = open(file, 'wb')
        version_file_write.write(sed_res_md5.encode('utf-8'))
        version_file_write.write(sed_res_ver.encode('utf-8'))
        version_file_write.close()
    elif ver_dict['lua'] is not None:
        old_lua_md5 = ver_dict['lua']['old_LobbyLuaMD5']
        lua_md5 = ver_dict['lua']['LobbyLuaMD5']
        old_lua_ver = ver_dict['lua']['old_LobbyLuaVersion']
        lua_ver = ver_dict['lua']['LobbyLuaVersion']
        sed_lua_md5 = dumps.replace(old_lua_md5, lua_md5)
        sed_lua_ver = dumps.replace('<LobbyLuaVersion>' + str(old_lua_ver), '<LobbyLuaVersion>' + str(lua_ver))
        version_file_write = open(file, 'wb')
        version_file_write.write(sed_lua_md5.encode('utf-8'))
        version_file_write.write(sed_lua_ver.encode('utf-8'))
        version_file_write.close()
    else:
        return


if __name__ == '__main__':
    ver_xml = 'version.xml'
    response = parse_xml(ver_xml)
    print(response)
    write_version(response, ver_xml)


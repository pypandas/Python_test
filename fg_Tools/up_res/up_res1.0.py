# -*- coding: utf-8 -*-
import os
import shutil
import zipfile
import logging
from datetime import datetime
import xml.etree.ElementTree as ET
import hashlib

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
LOG_TIME = str(datetime.now()).split('.')[0]


def res_file_path(res_path, up_path):
    # 遍历Android目录下的文件，过滤所有zip，解压
    and_res_zip = os.listdir(res_path)
    if len(and_res_zip) == 0:
        logging.debug('%s|%s resources not update!' % (LOG_TIME, res_path))
        # exit(0)
        return False
    # 解压zip
    for and_zip_file in and_res_zip:
        if and_zip_file.split('.')[-1] == 'zip':
            try:
                Zfile = zipfile.ZipFile(os.path.join(res_path, and_zip_file), 'r')
                for fileM in Zfile.namelist():
                    Zfile.extract(fileM, res_path)
                Zfile.close()
                os.remove(os.path.join(res_path, and_zip_file))
            except:
                logging.debug('%s|%s not found zip file! ' % (LOG_TIME, res_path))
        else:
            logging.debug('%s|%s dir not zipfile update!' % (LOG_TIME, res_path))

    # 遍历Android目录下的文件， 压缩成zip
    and_res_files = os.listdir(res_path)
    # 压缩
    for and_file in and_res_files:
        if os.path.isdir(os.path.join(res_path, and_file)):
            # 创建resources文件夹
            if not os.path.exists(os.path.join(res_path, and_file, 'resources')):
                os.makedirs(os.path.join(res_path, and_file, 'resources', 'resources'))
            else:
                shutil.rmtree(os.path.join(res_path, and_file, 'resources'))
                os.makedirs(os.path.join(res_path, and_file, 'resources', 'resources'))
            # 遍历更新资源文件夹
            and_res_up = os.listdir(os.path.join(res_path, and_file))
            for and_res in and_res_up:
                # 增量更新文件
                if and_res == 'resources':
                    continue
                else:
                    if os.path.isdir(os.path.join(res_path, and_file, and_res)):
                        try:
                            shutil.copytree(os.path.join(res_path, and_file, and_res),
                                            os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, and_res))
                            logging.debug('%s|%s dir update success!' % (LOG_TIME, and_res))
                        except:
                            try:
                                shutil.rmtree(os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, and_res))
                                shutil.copytree(os.path.join(res_path, and_file, and_res),
                                                os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, and_res))
                                logging.debug('%s|%s remove dir update success!' % (LOG_TIME, and_res))
                            except:
                                logging.debug('%s|%s update file fails ! ' % (LOG_TIME, and_res))
                    else:
                        try:
                            shutil.copyfile(os.path.join(res_path, and_file, and_res),
                                            os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, and_res))
                            logging.debug('%s|%s file update success' % (LOG_TIME, and_res))
                        except:
                            logging.debug('%s|%s update file fails ! ' % (LOG_TIME, and_res))
                # zip文件更新
                if and_res == 'lua':
                    os.mkdir(os.path.join(res_path, and_file, 'lua_bak'))
                    shutil.move(os.path.join(res_path, and_file, and_res),
                                os.path.join(res_path, and_file, 'lua_bak'))
                elif and_res == 'resources':
                    continue
                else:
                    shutil.move(os.path.join(res_path, and_file, and_res),
                                os.path.join(res_path, and_file, 'resources', 'resources'))
            if os.path.exists(os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file)):
                # 压缩, 删除, 更新 lua
                try:
                    shutil.make_archive(os.path.join(res_path, and_file, 'lua'), 'zip',
                                        root_dir=os.path.join(res_path, and_file, 'lua_bak'))
                    shutil.rmtree(os.path.join(res_path, and_file, 'lua_bak'))
                    os.remove(os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, 'lua.zip'))
                    shutil.move(os.path.join(res_path, and_file, 'lua.zip'),
                                os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file))
                except:
                    logging.debug('%s|%s not found lua dir!' % (LOG_TIME, and_file))

                # 压缩, 删除, 更新 resources
                shutil.make_archive(os.path.join(res_path, and_file, 'resources'), 'zip',
                                    root_dir=os.path.join(res_path, and_file, 'resources'))
                shutil.rmtree(os.path.join(res_path, and_file, 'resources'))
                os.remove(os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, 'resources.zip'))
                shutil.move(os.path.join(res_path, and_file, 'resources.zip'),
                            os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file))

                # 修改version文件, 判断该文件夹是否是大厅
                if is_number(and_file):
                    read_game_xml(os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file))
                else:
                    hall_files = os.listdir(os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file))
                    for i in hall_files:
                        if str(i).split('.')[-1] == 'xml':
                            phonename = 'Phone' + i[7:][:-3] + 'zip'
                            filemd5 = file_md5(
                                os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, phonename))
                            xmlpath = os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file, i)
                            read_hall_xml(filemd5, xmlpath,
                                          os.path.join(os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file)))
            else:
                logging.debug('%s|%s is not found, please make dir!' % (
                    LOG_TIME, os.path.join('../', 'Phone', 'AssetBundle', up_path, and_file)))
            # 删除文件夹
            shutil.rmtree(os.path.join(res_path, and_file))


def read_hall_xml(md5str, xmlpath, respath):
    try:
        tree = ET.ElementTree()
        tree.parse(xmlpath)
        temp = tree.getroot()
        luamd5 = file_md5(os.path.join(respath, 'lua.zip'))
        resmd5 = file_md5(os.path.join(respath, 'resources.zip'))
        luavesion = int(temp.find('LobbyLuaVersion').text)
        resvesion = int(temp.find('LobbyResVersion').text)
        phonevesion = int(temp.find('LobbyPhoneZipVersion').text)
        if write_xml(xmlpath, str(temp.find('LobbyPhoneZipMD5').text), md5str):
            write_xml(xmlpath, '<LobbyPhoneZipVersion>' + str(phonevesion),
                      '<LobbyPhoneZipVersion>' + str(phonevesion + 1))
        if write_xml(xmlpath, str(temp.find('LobbyLuaMD5').text), luamd5):
            write_xml(xmlpath, '<LobbyLuaVersion>' + str(luavesion),
                      '<LobbyLuaVersion>' + str(luavesion + 1))
        if write_xml(xmlpath, str(temp.find('LobbyResMD5').text), resmd5):
            write_xml(xmlpath, '<LobbyResVersion>' + str(resvesion),
                      '<LobbyResVersion>' + str(resvesion + 1))
        logging.debug('%s|%s hall xml change success' % (LOG_TIME, xmlpath))
    except:
        logging.debug('%s|%s hall xml change fails' % (LOG_TIME, xmlpath))


def read_game_xml(file_path):
    tree = ET.ElementTree()
    xml_path = os.path.join(file_path, 'version.xml')
    lua_path = os.path.join(file_path, 'lua.zip')
    resources_path = os.path.join(file_path, 'resources.zip')
    try:
        tree.parse(xml_path)
        temp = tree.getroot()
        # 修改lua md5
        if os.path.exists(lua_path):
            lua_md5 = file_md5(lua_path)
            lus_version = int(temp.find('LobbyLuaVersion').text)
            if write_xml(xml_path, str(temp.find('LobbyLuaMD5').text), lua_md5):
                write_xml(xml_path, '<LobbyLuaVersion>' + str(lus_version),
                          '<LobbyLuaVersion>' + str(lus_version + 1))
                logging.debug('%s|%s|lua md5 change success!' % (LOG_TIME, xml_path))

        # 修改resources md5
        res_md5 = file_md5(resources_path)
        res_version = int(temp.find('LobbyResVersion').text)
        if write_xml(xml_path, str(temp.find('LobbyResMD5').text), res_md5):
            write_xml(xml_path, '<LobbyResVersion>' + str(res_version),
                      '<LobbyResVersion>' + str(res_version + 1))
            logging.debug('%s|%s|resources md5 change success!' % (LOG_TIME, xml_path))
    except:
        logging.debug('%s|%s not found or damage!' % (LOG_TIME, xml_path))


def write_xml(file, old_str, new_str):
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


def file_md5(zip_file):
    fp = open(zip_file, 'rb')
    content = fp.read()
    fp.close()
    return hashlib.md5(content).hexdigest()


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


if __name__ == '__main__':
    res_file_path('android', 'Android5.0')
    res_file_path('ios', 'IOS5.0')

    # window
    os.system('pause')

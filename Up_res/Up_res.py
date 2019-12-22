# -*- encoding: utf-8 -*-
import os
import hashlib
from xml.etree.ElementTree import parse


def read_files_md5(path, file_ext, is_md5=True):
    files_md5_list = []
    files_md5_dict = {}
    path = os.listdir(path)
    for file in path:
        if str(file).split('.')[-1] == file_ext:
            pathname = os.path.join('./', file)
            fp = open(pathname, 'rb')
            contents = fp.read()
            fp.close()
            file_md5 = hashlib.md5(contents).hexdigest()
            file_name = file
            files_md5_list.append(file_name)
            files_md5_dict[file_name] = file_md5
    if is_md5:
        return files_md5_dict
    return files_md5_list


def read_xml_files_md5(xml_name, res):
    phone_name = 'Phone_' + str(str(xml_name).split('_')[-1]).split('.')[0] + '.zip'
    dom = parse(xml_name)
    root = dom.getroot()
    xml_md5_dict = {'resources.zip': root.find('LobbyResMD5').text, 'lua.zip': root.find('LobbyLuaMD5').text,
                    phone_name: root.find('LobbyPhoneZipMD5').text, }
    if xml_md5_dict['resources.zip'] != res['resources.zip']:
        root.find('LobbyResMD5').text = str(res['resources.zip'])
        root.find('LobbyResVersion').text = str(int(root.find('LobbyResVersion').text) + 1)
    if xml_md5_dict['lua.zip'] != res['lua.zip']:
        root.find('LobbyLuaMD5').text = str(res['lua.zip'])
        root.find('LobbyLuaVersion').text = str(int(root.find('LobbyLuaVersion').text) + 1)
    if xml_md5_dict[phone_name] != res[phone_name]:
        root.find('LobbyPhoneZipMD5').text = str(res[phone_name])
        root.find('LobbyPhoneZipVersion').text = str(int(root.find('LobbyPhoneZipVersion').text) + 1)
    else:
        print('暂无更新内容！')
    dom.write(xml_name, xml_declaration=True, encoding="utf-8", method="xml")


if __name__ == '__main__':
    file_dict = {}
    file_zip_dict = read_files_md5('./', 'zip', True)
    for one_zip_file in file_zip_dict:
        file_dict[one_zip_file] = file_zip_dict[one_zip_file]

    for one_xml_file in read_files_md5('./', 'xml', False):
        read_xml_files_md5(one_xml_file, file_dict)

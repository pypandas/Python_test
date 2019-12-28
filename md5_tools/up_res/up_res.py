import os
import hashlib
import zipfile
import shutil
import xml.etree.ElementTree as ET


def file_md5(zip_file):
    """
    获取文件MD5值
    :param zip_file: 文件路径
    :return:
    """
    fp = open(zip_file, 'rb')
    content = fp.read()
    fp.close()
    return hashlib.md5(content).hexdigest()


def zip_unzip():
    """
    1. files获取文件列表，遍历，判断zip是否是游戏资源，如果是则删除原有的lua.zip 和 resources.zip。解压游戏zip
    2. files1获取文件列表，遍历，判断游戏zip解压后的目录是否是存在，如果存在则在资源文件夹中创建resource文件夹
    3. files2获取文件列表，遍历，将lua之外的文件夹移动至resources文件夹，压缩lua和resources文件夹，删除不必要的文件及文件夹
    :return:
    """
    # 遍历当前目录
    files = os.listdir('./')
    for file in files:
        if (file.split('.')[-1] == 'zip' and file != 'lua.zip' and file != 'resources.zip') or os.path.isdir(file):

            # 删除原有zip
            try:
                os.remove('lua.zip')
            except:
                print('lua.zip 已被删除')
            try:
                os.remove('resources.zip')
            except:
                print('resources.zip 已被删除')

            # 将zip解压到当前目录
            try:
                zFile = zipfile.ZipFile(file, 'r')
                for fileM in zFile.namelist():
                    zFile.extract(fileM, './')
                zFile.close()
                os.remove(file)
            except:
                print('无压缩包更新')

            files1 = os.listdir('./')
            # 创建resources文件夹
            for file1 in files1:
                if os.path.isdir(file1) and float(file1):
                    if not os.path.exists(os.path.join(file1, 'resources')):
                        os.mkdir(os.path.join(file1, 'resources'))
                    else:
                        shutil.rmtree(os.path.join(file1, 'resources'))
                        os.mkdir(os.path.join(file1, 'resources'))

                    # 将除了lua和version.xml之外的文件和文件夹移至resources
                    files2 = os.listdir(os.path.join('./', file1))
                    for file2 in files2:
                        if file2.split('.')[-1] == 'xml':
                            continue
                        elif file2 == 'lua':
                            continue
                        else:
                            try:
                                shutil.move(os.path.join(file1, file2),
                                            os.path.join(file1, 'resources'))
                            except:
                                if os.path.exists(os.path.join(file1, file2)):
                                    shutil.rmtree(os.path.join(file1, file2))
                                else:
                                    os.remove(os.path.join(file1, file2))

                    # 压缩lua文件夹
                    if os.path.exists(os.path.join(file1, 'lua')):
                        shutil.make_archive('lua', 'zip', root_dir=os.path.join(file1, 'lua'))
                    else:
                        print(os.path.join(file1), '非lua游戏')

                    # 压缩resources文件夹
                    shutil.make_archive('resources', 'zip', root_dir=os.path.join(file1, 'resources'))

                    # 删除lua和resources文件夹
                    shutil.rmtree(os.path.join(file1))
                    print(os.path.join(file1), '资源更新完成')

        else:
            continue


def read_xml(xml_path):
    """
    解析version.xml文件
    :param xml_path: xml文件路径
    :return:
    """
    tree = ET.ElementTree()
    try:
        tree.parse(xml_path)
        temp = tree.getroot()
        # 修改lua md5
        if os.path.exists('lua.zip'):
            lua_md5 = file_md5('lua.zip')
            lus_version = int(temp.find('LobbyLuaVersion').text)
            if write_xml(xml_path, str(temp.find('LobbyLuaMD5').text), lua_md5):
                write_xml(xml_path, '<LobbyLuaVersion>' + str(lus_version),
                          '<LobbyLuaVersion>' + str(lus_version + 1))
                print('lua md5 修改成功')

        # 修改resources md5
        res_md5 = file_md5('resources.zip')
        res_version = int(temp.find('LobbyResVersion').text)
        if write_xml(xml_path, str(temp.find('LobbyResMD5').text), res_md5):
            write_xml(xml_path, '<LobbyResVersion>' + str(res_version),
                      '<LobbyResVersion>' + str(res_version + 1))
            print('resources md5 修改成功')
    except:
        print('version.xml文件损坏')


def write_xml(file, old_str, new_str):
    """
    修改xml文件内容
    :param file: 文件路径
    :param old_str: 文件被修改内容
    :param new_str: 文件修改的新内容
    :return: 1，有内容修改 0，无内容修改
    """
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
    zip_unzip()
    read_xml('./version.xml')

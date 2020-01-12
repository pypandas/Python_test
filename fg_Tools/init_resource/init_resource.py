import os
import logging
import datetime
import shutil

logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')
LOG_TIME = str(datetime.datetime.now()).split('.')[0]


def res_dir(res_path):
    for root_path in os.listdir(os.path.join('../', 'Phone', 'AssetBundle', res_path)):
        try:
            os.mkdir(os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, 'version_1'))
            logging.info('%s|SUCCESS|%s __init__ success' % (
                LOG_TIME, os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, 'version_1')))
        except:
            if os.path.exists(os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, 'version_1')):
                logging.info('%s|INFO|%s not __init__' % (
                    LOG_TIME, os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, 'version_1')))
            else:
                logging.error('%s|ERROR|%s make dir fails')

        for game_res in os.listdir(os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path)):
            if game_res.split('.')[-1] == 'xml':
                write_xml(os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, game_res))
                logging.info('%s|INFO|%s add new update field' % (
                    LOG_TIME, os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, game_res)))
            elif game_res != 'version_1' and game_res.split('.')[-1] != 'xml':
                shutil.move(os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, game_res),
                            os.path.join('../', 'Phone', 'AssetBundle', res_path, root_path, 'version_1'))
            else:
                continue


def write_xml(write_path):
    file = open(write_path, 'rb')
    r = file.readlines()
    file.close()
    w_file = open(write_path, 'wb')
    for i in r:
        if i.decode('utf-8').find('<LobbyHallVersion>') == -1:
            if i.decode('utf-8') != '</ROOT>':
                w_file.write(i)

            elif i.decode('utf-8') == '</ROOT>':
                w_file.write('  <LobbyHallVersion>1</LobbyHallVersion> <!-- 新资源更新版本号 --> \n'.encode('utf-8'))
                w_file.write('</ROOT>'.encode('utf-8'))
        else:
            continue
    w_file.close()


if __name__ == "__main__":
    res_dir('Android5.0')
    res_dir('IOS5.0')

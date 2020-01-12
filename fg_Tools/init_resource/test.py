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


write_xml('version.xml')

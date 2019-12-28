import zipfile
import os


def get_zip_file(zip_file_name):
    zFile = zipfile.ZipFile(zip_file_name + '.zip', 'w')
    for root, _, file in os.walk(zip_file_name):
        zFile.write(root)
        for i in file:
            print(os.path.join(root, i))
            zFile.write(os.path.join(root, i))
    zFile.close()


get_zip_file('10300177')

import os
import shutil


# shutil.move('up_res.log', 'android')

try:
    shutil.copytree('cs', 'android/cs')
except:
    shutil.rmtree('android/cs')
    shutil.copytree('cs', 'android/cs')
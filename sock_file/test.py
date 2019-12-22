import time
import sys


def progress_test():
    bar_length = 20
    # for percent in range(0, 101):
    hashes = ' ' * int(40 / 100 * 50)
    print(len(hashes))
    spaces = '#' * (50 - len(hashes))
    sys.stdout.write("\rPercent: [%s] %d%%" % (spaces + hashes, 100 - len(hashes) * 2))
    sys.stdout.flush()


progress_test()

'''
程序入口
'''


import os
import sys
from cron import src


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


if __name__ == '__main__':
    pass
src.run()
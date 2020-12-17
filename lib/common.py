'''
公共功能
'''
import logging.config,time
from conf import setting
from cron import src
from db import db_handler

res = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

# 登入认证装饰器
def login_auth(func):
    def wrapper(*args,**kwargs):
        if not src.login_user["name"] is None:
            return func(*args,**kwargs)
        else:
            print("请登入后使用该功能")
            src.login()
    return wrapper


# 日志记录功能
def loggin_record(name):
    logging.config.dictConfig(setting.LOGGING_DIC)  # 使用这个日志字典
    logger = logging.getLogger(name)  # 实例出日志对象
    return logger

user_loggin = loggin_record('login')


# 用户锁定功能
def locker(name):
    user_dic = db_handler.check(name)
    user_dic["lock"] = True
    db_handler.save(user_dic)
    user_loggin.info(f'用户{name}已被锁定')
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 当前用户{name}已被锁定")
    return

# 解锁用户功能
def unlock(name):
    user_dic = db_handler.check(name)
    user_dic["lock"] = False
    user_loggin.info(f'用户{name}已经解除解锁')
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 当前用户{name}已经解除解锁")
    db_handler.save(user_dic)
    return

# 进度条
def progress(percent, symbol='█', width=50):
    if percent > 1:
        percent = 1
    show_progress = ("|%%-%ds|" % width) % (int(percent * width) * symbol)
    print("\r%s %.2f%%" % (show_progress, percent * 100), end='')

def plan():
    data_size = 1025
    recv_size = 0
    while recv_size < data_size:
        time.sleep(0.1) # 模拟数据的传输延迟
        recv_size+=150 # 每次收1024

        percent=recv_size / data_size # 接收的比例
        progress(percent, width=50) # 进度条的宽度70
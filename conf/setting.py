'''
日志字典配置
'''
import os

BASE_PATH = os.path.normpath(os.path.join(__file__,"..",".."))
DB_PATH = os.path.join(BASE_PATH,'db')
LOG_PATH = os.path.join(BASE_PATH,'log')
ROOT_PATH = os.path.join(BASE_PATH,'db','root')

# 判断日志文件夹是否存在,不存在新建一个
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)



#🍚自定义日志的输出格式
formatter1_format = '%(asctime)s %(name)s %(levelname)s:  %(message)s'
formatter2_format = '%(asctime)s %(name)s %(levelname)s:  %(message)s'
formatter3_format = '%(asctime)s %(name)s %(levelname)s:  %(message)s'

#🍚通过变量的方式存放路径,也可以使用"os.path"来规范路径
# logfile_path2 = r'F:\Pycharm File\PycharmProjects\python正课\day18\a2.log'  # log文件名
login_log = os.path.join(LOG_PATH,'login.log')  # log文件名
transaction_log = os.path.join(LOG_PATH,'transaction.log')  # log文件名
default_log = os.path.join(LOG_PATH,'default.log')  # log文件名

#🍚log配置字典, 里面就是上面提到的四种对象
LOGGING_DIC = {
    'version': 1,                       # 指定版本信息
    'disable_existing_loggers': False,  # 关闭已存在日志。默认False
#    🔰控制日志的格式
    'formatters': {                      # 固定格式不能修改
        "formatter1": {                  # 开头自定义的日志输出格式名
            'format': formatter1_format  # "format" 固定格式不能修改
        },
        'formatter2': {
            'format': formatter2_format
        },
        'formatter3': {
            'format': formatter3_format
        },
    },
#    🔰过滤日志 (不常用)
    'filters': {},
#    🔰控制日志输出的位置
    'handlers': {
        'login_handler': {                   # 自定义"handlers"名字,可以改
            'level': 'DEBUG',                # 日志过滤等级
            'class': 'logging.FileHandler',  # 保存到文件里面去(日志保存的形式)
            'formatter': 'formatter1',       # 绑定的日志输出格式
            'filename': login_log,       # 制定日志文件路径
            'encoding': 'utf-8',             # 日志文件的编码，不再担心乱码问题
        },
        'transaction_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'formatter2',
            'filename': transaction_log,
            'encoding': 'utf-8',
        },
        'default_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'formatter2',
            'filename': default_log,
            'encoding': 'utf-8',
        },
        'terminal': {                        # 自定义的"handlers"名字(终端)
            'level': 'DEBUG',                # 日志过滤等级
            'class': 'logging.StreamHandler',# 打印到屏幕
            'formatter': 'formatter3'        # 日志输出格式
        },
    },
#    🔰负责生产日志
    'loggers': {
        # '' 代表默认的,在执行'logging.getLogger("key")'时,在"loggers"里面没有找到这个"key"时就使用这个
        '': {
            # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'handlers': ['default_handler','terminal'],
            'level': 'DEBUG',
            'propagate': False,  # 向上(更高level的logger)传递,默认True, 通常设置为False
        },
        # 在执行'logging.getLogger("key")'时,在"loggers"里面找到这个"key"时就使用这个
        'login': {
            'handlers': ['login_handler','terminal'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'transaction': {
            'handlers': ['transaction_handler','terminal'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
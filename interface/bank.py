import os,time
from db import db_handler
from conf import setting
from lib import common

bank_loggin = common.loggin_record('transaction')


def balance_api(name):
    '''
    查询余额接口
    :param name:
    :return:
    '''
    user_dic = db_handler.check(name)
    bank_loggin.info(f"用户:{name}查看了余额")
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 我查看了余额")
    db_handler.save(user_dic)
    return user_dic["balan"]



def transfer_api(from_name,to_name,money):
    '''
    转账接口
    :param fron_name:
    :param to_name:
    :return:
    '''
    user_dic = db_handler.check(from_name)
    to_user_path = os.path.join(setting.DB_PATH,f"{to_name}.json")
    if os.path.isfile(to_user_path):
        from_dic = db_handler.check(from_name)
        to_dic = db_handler.check(to_name)
        if from_dic["balan"] >= money*1.05:
            from_dic["balan"] -= money*1.05
            to_dic["balan"] += money
            from_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 我向用户:{to_name}转账了{money}元,扣除了手续费{money * 0.05:.2f}元")
            db_handler.save(from_dic)
            to_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 用户:{from_name}向我转账了{money}元")
            db_handler.save(to_dic)
            bank_loggin.info(f"用户:{from_name}向用户:{to_name}转账了{money}元,扣除了手续费{money * 0.05:.2f}元")
            return True,"转账成功"
        else:
            return False,"余额不足"
    else:
        return False,"对方用户账号不存在"


def withdraw_api(name,money):
    '''
    取款接口
    :param name:
    :param money:
    :return:
    '''
    user_dic = db_handler.check(name)
    if user_dic["balan"] >= money*1.05:
        user_dic["balan"] -= money*1.05
        user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 我从账户中取走了:{money}元,扣除手续费:{money*0.05:.2f}元")
        db_handler.save(user_dic)
        bank_loggin.info(f"用户:{name}从账户中取走了:{money}元,扣除手续费:{money*0.05:.2f}元")
        return True,"取款成功"
    else:
        return False,"余额不足"


def deposit_api(name,money):
    '''
    存款接口
    :param name:
    :param money:
    :return:
    '''
    user_dic = db_handler.check(name)
    user_dic["balan"] += money
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 我存入了:{money}元到账户")
    db_handler.save(user_dic)
    bank_loggin.info(f"用户:{name}存入了:{money}元到账户")
    return "存款成功"


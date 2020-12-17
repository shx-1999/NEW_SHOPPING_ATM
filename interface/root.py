'''
管理员功能接口
'''
import os,json
from conf import setting
from db import db_handler
from lib import common
from cron import src

root_loggin = common.loggin_record("root")


# 管理员登入接口
def root_login(name,passwd):
    root_path = os.path.join(setting.ROOT_PATH,f'{name}.json')
    if os.path.isfile(root_path):
        with open(rf"{root_path}","rt",encoding="utf-8")as f:
            root_dic = json.load(f)
            if name ==root_dic["name"] and passwd == root_dic["passwd"]:
                root_loggin.info("管理员进行了登入")
                return True,"验证成功"
            else:
                return False,"密码错误"
    else:
        return False,"该管理员不存在"


# 锁定接口
def lock_api(name):
    user_dic = db_handler.check(name)
    if user_dic:
        common.locker(name)
        root_loggin.info(f"管理员锁定了用户:{name}")
        return True,"锁定成功"
    else:
        return False,"该用户不存在"

# 解锁接口
def unlock_api(name):
    user_dic = db_handler.check(name)
    if user_dic:
        common.unlock(name)
        root_loggin.info(f"管理员对用户:{name}解除了锁定")
        return True,"解锁成功"
    else:
        return False,"该用户不存在"

# 修改用户额度接口
def change_api(name,money):
    user_dit = db_handler.check(name)
    if user_dit:
        user_dit["balan"] = money
        root_loggin.info(f"管理员修改了用户:{name}的账户余额,修改后余额为:{money}元")
        db_handler.save(user_dit)
        return True,"余额修改成功"
    else:
        return False,"该用户不存在"

# 删除用户
def remove_api(name):
    user_dit = db_handler.check(name)
    if user_dit:
        os.remove(os.path.join(setting.DB_PATH,f'{name}.json'))
        root_loggin.info(f"管理员删除了{name}用户信息")
        return True,"删除成功"
    else:
        return False,"该用户不存在"

# 添加用户
def add_name():
    name = src.register()
    return name
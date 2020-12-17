'''
查询和保存用户信息
'''
import os
import json
from conf import setting


def save(user_dic):
    '''
    用户文件修改
    :return:
    '''
    name = user_dic["name"]
    user_path = os.path.join(setting.DB_PATH,f"{name}.json")
    with open(user_path,"wt",encoding="utf-8")as f1:
        json.dump(user_dic,f1)
        f1.flush()



def check(name):
    '''
    查看用户信息
    :param name:
    :return:
    '''
    user_path = os.path.join(setting.DB_PATH,f'{name}.json')
    if os.path.isfile(user_path):
        with open(rf"{user_path}","rt",encoding="utf-8")as f:
            user_dic = json.load(f)
            return user_dic
    else:
        return None


# "shops": {"smoke": [20, 5]}
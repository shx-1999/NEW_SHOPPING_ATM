import time
from db import db_handler
from lib import common

shop_loggin = common.loggin_record('login')
ll = '\033[1;30;46m'
llll = '\033[1;36m'
rr = '\033[0m'

def check_shopping_card(name):
    '''
    查看购物车接口
    :param name:
    :return:
    '''
    user_dic = db_handler.check(name)
    shop_loggin.info(f"用户:{name}查看了购物车")
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 当前用户:{name}查看了购物车")
    db_handler.save(user_dic)
    return user_dic["shops"]

def shop_pay(name,consume,user_dic):
    '''
    购物支付接口
    :return:
    '''
    select = input("Y:结账/N:退出>>").strip()
    if select.lower() == "y":
        common.plan()
        print(f"\n{ll}本次购买商品:{rr}")
        for k, v in user_dic["shops"].items():
            print(f"{k:<11} price:{v[0]:<8} count:{v[1]:<2}")
        user_dic["balan"] -= consume
        shop_loggin.info(f"用户:{name}在商城消费了{consume}元")
        user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))} 当前用户:{name}在商城一共消费{consume}元")
        db_handler.save(user_dic);
        return True,f"您一共消费{llll}{consume}{rr}元\n欢迎下次光临!!"
    elif select.lower() == "n":
        return False,f"{ll}取消支付...{rr}欢迎下次光临!!"
    else:
        return None,"没有该选项"

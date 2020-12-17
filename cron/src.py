'''
程序核心逻辑+用户操作界面
'''
from interface import user,bank,shop,root
from db import db_handler
from lib import common
from conf import setting


ll = '\033[1;30;46m'
lll = '\033[1;31m'
llll = '\033[1;36m'
lllll = '\033[1;34m'
rr = '\033[0m'



# 判断用户是否登入
login_user = {"name":None}

# 退出登入
def logout():
    login_user["name"] = None
    common.plan()
    print(f"\n退出成功")

# 登入
def login():
    print(f"{ll}正在登入...{rr}")
    count = 0
    if not login_user["name"] is None:
        print("您已经登入了");return
    while 1:
        name = input("请输入用户名(q退出)>>").strip()
        if count == 3:
            common.locker(name);print("该用户错误次数过多,已锁定")
            break
        if name.lower() == "q": break
        passwd = input("请输入密码>>").strip()
        tf,result = user.login_api(name,passwd)
        if tf:
            login_user["name"] = name
            common.plan()
            print("\n",result);break
        else:
            if tf is False:
                count += 1
                print(f"{result},还剩{3-count}次机会")
            else:
                print(result)



# 注册
def register():
    if not login_user["name"] is None:
        print("您当前正在登入,请退出到初始界面注册用户");return
    common.plan()
    print(f"\n{ll}正在注册新账户...{rr}")
    print(f"注册须知：{lll}用户名必须大于3位，密码不能为空{rr}")
    while 1:
        name = input("请输入账号名(q退出)>>").strip()
        if name.lower() == "q":return
        if len(name) <= 3:
            print(f"{ll}用户名不能小于3位{rr}");continue
        passwd = input("请输入密码>>").strip()
        if len(passwd) == 0:
            print(f"{ll}密码不能为空{rr}");continue
        ok_passwd = input("请确认密码>>").strip()
        if passwd == ok_passwd:
            tf,result = user.register_api(name,passwd)
            if tf:
                print(result);return name
            else:
                print(result)
        else:
            print("两次密码不一致")



# 转账
@common.login_auth
def transfer():
    print(f"{ll}正在进入转账操作...{rr}")
    while True:
        to_name = input('输入转账的用户(q退出)>>:').strip()
        if to_name.lower() == "q":break
        money = input('输入转账金额>>:').strip()
        if money.isdigit():
            money = int(money)
            tf, result = bank.transfer_api(login_user['name'], to_name, money)
            if tf:
                common.plan()
                print("\n",result)
                break
            else:
                print(result)
        else:
            print('必须输入数字')

# 取款
@common.login_auth
def withdraw():
    while 1:
        balan = input("请输入取款金额(q退出)>>").strip()
        if balan.lower() == "q":break
        if balan.isdigit():
            balan = int(balan)
            tf,result = bank.withdraw_api(login_user["name"],balan)
            if tf:
                common.plan()
                print("\n",result);break
            else:
                print(result)
        else:
            print("请输入整数金额")

# 存款
@common.login_auth
def deposit():
    print(f"{ll}正在进入存款操作...{rr}")
    while 1:
        balan = input("请输入存入金额(q退出)>>").strip()
        if balan.lower() == "q":break
        if balan.isdigit():
            balan = int(balan)
            result = bank.deposit_api(login_user["name"],balan)
            common.plan()
            print("\n",result);break
        else:
            print("请输入整数金额")


# 查看余额
@common.login_auth
def balance():
    print(f"{ll}正在获取账户余额...{rr}\n");common.plan()
    user_balan = bank.balance_api(login_user["name"])
    print(f"当前账户余额:{llll}￥{user_balan}{rr}")


# 购物+支付
@common.login_auth
def shopping():
    print(f"{ll}梦想商城欢迎您{rr}\n")
    consume = 0
    user_dic = db_handler.check(login_user["name"])
    user_dic["shops"] = {}
    user_balan = user_dic["balan"]

    while 1:
        for k,v in enumerate(shop_dic):
            print(f"{lllll}{k:>3}  goods : {v[0]:<11} price : {v[1]:<5}{rr}")
        chiose = input("请选择商品编号q退出>>").strip()
        if chiose.isdigit():
            chiose = int(chiose)
            if chiose > len(shop_dic)-1:
                print("未找到此商品");continue
            good_name = shop_dic[chiose][0]
            good_price = shop_dic[chiose][1]
            if user_balan >= good_price:
                user_balan -= good_price
                if good_name in user_dic["shops"]:
                    user_dic["shops"][good_name][1] += 1
                    consume += good_price
                else:
                    consume +=good_price
                    user_dic["shops"][good_name] = [good_price,1]
                print(f"商品{ll}{good_name}{rr}已加入购物车")
            else:
                print(f"{ll}余额不足!{rr}穷鬼")
        elif chiose.lower() == "q":
            if len(user_dic["shops"]) == 0:
                print(f"{ll}您未购买任何物品{rr}欢迎下次光临!!");break
            tf,result = shop.shop_pay(login_user["name"],consume,user_dic)
            if tf:
                print(result);break
            elif tf is False:
                print(result);break
            else:
                print(result);continue
        else:
            print("请输入数字")



# 查看购物车
@common.login_auth
def shopping_cart():
    user_shops = shop.check_shopping_card(login_user["name"])
    if len(user_shops) == 0:
        print(f"{ll}您什么都没有买{rr}")
    else:
        print(f"{ll}您购买的商品:{rr}")
        for k,v in user_shops.items():
            print(f"{llll}{k:<11}单价:{v[0]:<9}个数:{v[1]:<3}总价:{v[0]*v[1]}元{rr}")


# 查看个人操作日志
@common.login_auth
def check_active():
    log_file = user.user_active(login_user["name"])
    for i in log_file:
        print(f"{llll}{i}{rr}")





# 管理员登录
def root_login():
    if not login_user["name"] is None:
        print("您当前正在登入,请退出到初始界面进行登入");
        return
    while 1:
        print(f"{ll}管理员登入...{rr}")
        root_name= input("请输入管理员账户(q退出)>>").strip()
        if root_name.lower() == "q":return
        root_passwd= input("请输入管理员密码>>").strip()
        tf,result = root.root_login(root_name,root_passwd)
        if tf:
            common.plan()
            print("\n",result)
            root_select()
            break
        else:
            print(result)



# 锁定用户
def root_lock():
    lock_name = input("请输入需要锁定的用户名>>").strip()
    tf,result = root.lock_api(lock_name)
    if tf:
        common.plan()
        print("\n",result)
        return
    else:
        print(result)

# 解锁用户
def root_unlock():
    lock_name = input("请输入需要解锁的用户名>>").strip()
    tf, result = root.unlock_api(lock_name)
    if tf:
        common.plan()
        print("\n",result)
        return
    else:
        print(result)

# 修改用户额度
def root_change_money():
    name = input("请输入需要更改的余额的账户>>").strip()
    money = input("请输入该用户修改后余额>>").strip()
    if money.isdigit():
        money = int(money)
        tf,result = root.change_api(name,money)
        if tf:
            common.plan()
            print("\n",result)
            return
        else:
            print(result)
    else:
        print("请输入整数")

# 添加用户
def add_user():
    name = root.add_name()
    if name is None:
        pass
    else:
        root.root_loggin.info(f"管理员添加了用户:{name}")




def remove_user():
    name = input("请输入需要删除的账户>>").strip()
    y_n = input(f"{llll}请再次确认Y/其他键取消>>{rr}").strip()
    if y_n.lower() == "y":
        tf,result = root.remove_api(name)
        if tf:
            common.plan()
            print("\n",result)
        else:
            print(result)
    else:
        print("您取消了删除用户操作")

# 查看金额流动日志
def monry_log():
    with open(rf"{setting.transaction_log}","rt",encoding="utf-8")as f:
        for i in f:
            print(f"{lll}{i.strip()}{rr}")

# 查看用户操作日志
def user_log():
    with open(rf"{setting.login_log}", "rt", encoding="utf-8")as f:
        for i in f:
            print(f"{lll}{i.strip()}{rr}")

# 查看管理员日志
def root_log():
    with open(rf"{setting.default_log}", "rt", encoding="utf-8")as f:
        for i in f:
            print(f"{lll}{i.strip()}{rr}")


root_function = [
    ["锁定用户",root_lock],
    ["解锁用户",root_unlock],
    ["修改用户额度",root_change_money],
    ["添加用户",add_user],
    ["删除用户",remove_user],
    ["查看金额流动日志",monry_log],
    ["查看用户操作日志",user_log],
    ["查看管理员日志",root_log],
]


def root_select():
    common.plan()
    print(f"\n{ll}欢迎进入管理员界面...{rr}")
    while 1:
        for i, v in enumerate(root_function):
            print(f"{i:<3} {str(v[0]):<5}")
        chiose = input("请选择功能(q退出)>>").strip()
        if chiose.lower() == "q":return
        if chiose.isdigit():
            chiose = int(chiose)
            if not chiose >= len(root_function):
                root_function[chiose][1]()
            else:
                print("请输入存在编号")
        else:
            print("请输入数字")





msg_dic = {
    "0" : [logout,"退出登入"],
    "1" : [login,"登入"],
    "2" : [register,"注册"],
    "3" : [transfer,"转账"],
    "4" : [withdraw,"取款"],
    "5" : [deposit,"存款"],
    "6" : [balance,"查看余额"],
    "7" : [shopping,"购物"],
    "8" : [shopping_cart,"查看购物车"],
    "9" : [check_active,"查看个人流水"],
    "10" : [root_login,"管理员入口"],
}

shop_dic = [
    ["aircraft" , 29988888],
    ["cottage" , 9999999],
    ["Rolls-Royce" , 25555555],
    ["Rolex" , 100000],
    ["yacht" , 322000],
    ["Halley" , 2000000],
    ["smoke" , 20],
]

photo = f'''{llll}
    ╭╮╭╮ ╭━━╮ ╭━━╮ ╭━━╮ ╭╮╭╮
    ┃┃┃┃ ┃╭╮┃ ┃╭╮┃ ┃╭╮┃ ┃╰╯┃
    ┃╰╯┃ ┃╰╯┃ ┃╰╯┃ ┃╰╯┃ ╰╮╭╯
    ┃╭╮┃ ┃╭╮┃ ┃╭━╯ ┃╭━╯  ┃┃　
    ┃┃┃┃ ┃┃┃┃ ┃┃   ┃┃    ┃┃　
    ╰╯╰╯ ╰╯╰╯ ╰╯   ╰╯    ╰╯
　╭╩═╮╔════╗╔════╗╔════╗╔════╗╔════╗   
╭╯GO ╠╣海绵宝宝╠╣欢迎欢迎╠╣派大猩猩╠╣章鱼哥哥╠╣蟹黄宝宝║
╰⊙═⊙╯╚◎══◎╝╚◎══◎╝╚◎══◎╝╚◎══◎╝╚◎══◎╝{rr}'''


def run():
    print(f"\033[1;30;42m欢迎进入派大星一体式商城,祝您购物愉快\033[0m\n{photo}")
    while 1:
        for k,v in msg_dic.items():
            print(f"{lll}  {k:<4} {v[1]:<7}{rr}")
        print(f"{lll}  11   退出商城{rr}")
        count = input("请选择服务编号>>").strip()
        if count == "11":
            print("正在退出...\n");common.plan();break
        if count in msg_dic:
            msg_dic[count][0]()
        else:
            print("请输入存在功能")




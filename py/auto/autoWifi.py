import requests
import time
import subprocess
import os
import sys
import keyboard
import winreg as reg
import simplejson as json
from colorama import init, Fore, Style
from urllib.parse import urlencode
import logging
from datetime import datetime

init(autoreset=True)
v = "v1.5"

# 函数定义区

def clear_screen():
    """跨平台清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_program_path():
    if getattr(sys, 'frozen', False):
        # 当被打包为 EXE 时
        return os.path.dirname(os.path.realpath(sys.executable))
    else:
        # 直接从源代码运行时
        return os.path.dirname(os.path.abspath(__file__))

def autoStart():
    # 获取当前程序的完整路径
    program_path = sys.argv[0] 
    print(program_path)
    
    # 获取程序名称
    program_name = os.path.basename(program_path)
    print(program_name)

    # 打开注册表
    try:
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(registry_key, program_name, 0, reg.REG_SZ, program_path)  # 使用程序名称作为注册表的键
        reg.CloseKey(registry_key)
        print(f"{program_name} 已成功添加到开机自启!")
    except Exception as e:
        print(f"添加到开机自启失败: {e}")

def printLog(mode=1):
    """增强版日志输出函数
    :param mode: 1-默认LOGO, 2-连接失败, 3-连接成功
    """
    # 定义不同模式的字符画
    status_art = {
        1: (
            "    █████╗   ██╗   ██╗  ████████╗   ██████╗   ██╗    ██╗  ██╗  ███████╗  ██╗\n"
            "   ██╔══██╗  ██║   ██║  ╚══██╔══╝  ██╔═══██╗  ██║    ██║  ██║  ██╔════╝  ██║\n"
            "   ███████║  ██║   ██║     ██║     ██║   ██║  ██║ █╗ ██║  ██║  █████╗    ██║\n"
            "   ██╔══██║  ██║   ██║     ██║     ██║   ██║  ██║███╗██║  ██║  ██╔══╝    ██║\n"
            "   ██║  ██║  ╚██████╔╝     ██║     ╚██████╔╝  ╚███╔███╔╝  ██║  ██║       ██║\n"
            "   ╚═╝  ╚═╝  ╚═════╝       ╚═╝      ╚═════╝    ╚══╝╚══╝   ╚═╝  ╚═╝       ╚═╝"
        ),
        2: (
            "███████╗   █████╗   ██╗  ██╗       ██████╗ \n"
            "██╔════╝  ██╔══██╗  ██║  ██║       ██╔══██╗\n"
            "█████╗    ███████║  ██║  ██║       ██║  ██║\n"
            "██╔══╝    ██╔══██║  ██║  ██║       ██║  ██║\n"
            "██║       ██║  ██║  ██║  ███████╗  ██████╔╝\n"    
            "╚═╝       ╚═╝  ╚═╝  ╚═╝  ╚══════╝  ╚═════╝ "
        ),
        3: (
            "███████╗  ██╗   ██╗   ██████╗  ███████╗  ███████╗  ███████╗\n"
            "██╔════╝  ██║   ██║  ██╔════╝  ██╔════╝  ██╔════╝  ██╔════╝\n"
            "███████╗  ██║   ██║  ██║       █████╗    ███████╗  ███████╗\n"
            "╚════██║  ██║   ██║  ██║       ██╔══╝    ╚════██║  ╚════██║\n"
            "███████║  ╚██████╔╝  ╚██████╗  ███████╗  ███████║  ███████║\n"
            "╚══════╝   ╚═════╝    ╚═════╝  ╚══════╝  ╚══════╝  ╚══════╝"
        )
    }

    # 设置颜色方案
    color_schemes = {
        1: [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA],
        2: [Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW],
        3: [Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.CYAN]
    }

    text = status_art[mode]
    colors = color_schemes[mode]
    color_count = len(colors)

    # 清屏并打印字符画
    clear_screen()
    print("-"*20)
    print(f"自动连接校园网程序 {v}  使用过程中遇到bug请反馈给你这个程序的人")
    print(f"假设重新启动计算机后，未运行此程序，请在防火墙中为程序添加白名单，或者安装火绒安全")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        color_offset = i % color_count
        for j, char in enumerate(line):
            color = colors[(j + color_offset) % color_count]
            print(f"{color}{char}", end="")
        print()
    print(Style.RESET_ALL)

def selectTorF(text, opt0, opt1, res=0):
    print("\r" + " " * (len(text) + len(opt0) + len(opt1) + 10), end="\r")
    
    def keyDown(e):
        nonlocal res
        # 切换结果为0和1
        res = 0 if res == 1 else 1 
        # 打印当前选择的选项
        if res == 0:
            print(f"\r{text} {Fore.RED+opt0}", end="")
        else:
            print(f"\r{text} {Fore.GREEN+opt1}", end="")    

    print(f"\r{text} {Fore.RED+opt0}", end="")
    keyboard.on_press_key("down", keyDown)

    # 继续监听'enter'键
    keyboard.wait('enter')
    keyboard.unhook_all()
    input()
    return res

def Login(SID, PW):
    url = "http://dr.com/drcom/login?callback=dr1003"
    data = {
        "DDDDD": f"{SID}@unicom",
        "upass": PW,
        "0MKKey": "123456",
        "R1": "0",
        "R2": "",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "v6ip": "",
        "terminal_type": "1",
        "lang": "zh-cn",
        "jsVersion": "4.2",
        "v": "3144"
    }
    
    response = requests.post(url, data=data)
    if "成功" in response.text: 

        print("登录成功")
        full_url = f"{url}&{urlencode(data)}"
        # print(f"请求的完整 URL: {full_url}")
        return True
    else:
        print(f"登录失败")
        return False

def connect_to_wifi(ssid):
    # 创建连接WiFi的命令    
    command = f'netsh wlan connect name="{ssid}"'
    
    # 使用subprocess调用命令
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # 输出结果
    if result.returncode == 0:
        print(f"成功连接到 WiFi: {ssid}")
        return True
    else:
        print(f"连接失败: {result.stderr}")
        return False

def initP(b):
    printLog()
    

    # 打印斜着渐变效果的文本
    

    while True:
        if not b:
            with open(config_path) as f:
                config = json.load(f)
                isorno = config['isAutoStart']
        SID = input("输入您的学号（例如20242753xxxx）: ")
        password = input("请输入校园网密码: ")
        if b:
            isorno = selectTorF("是否开机自启？？方向键下选择↓,回车确认）", "否", "是")
        
        print("\n", "-"*20)
        print(f"\t您的学号是{SID}\n\t您的密码是{password}")
        print(f"\t确认开机自启： {'是' if isorno else '否'}" if b else "")
        queren = selectTorF("是否确认上面的信息（方向键下选择↓,回车确认）", "重新输入", "确认")
        if queren == 1:  # 如果选择确认
            break  # 退出循环

    return [SID, password, isorno]

def initC(config):  # 初始化并写入值
    script_directory = get_program_path()  # 获取脚本所在目录
    config_path = os.path.join(script_directory, 'config.json')  # 生成绝对路径

    with open(config_path, 'w') as f:
        json.dump(config, f)

# 配置日志记录
log_directory = get_program_path()  # 获取程序目录
if not os.path.exists(os.path.join(log_directory, '崩溃日志')):
    os.makedirs(os.path.join(log_directory, '崩溃日志'))

# 创建一个日志记录器
logger = logging.getLogger('autoWifiLogger')
logger.setLevel(logging.DEBUG)

# 创建一个文件处理器来记录日志
log_file_path = os.path.join(log_directory, 'log.txt')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

# 创建一个控制台处理器来输出日志到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.exit(0)
    
    # 使用 sys.exc_info() 以获取当前异常信息
    logger.error("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
    
    # 将未捕获的异常信息写入崩溃日志文件
    crash_time = datetime.now().strftime('%Y%m%d%H%M%S')
    crash_log_path = os.path.join(log_directory, '崩溃日志', f'crash_report_{crash_time}.txt')
    with open(crash_log_path, 'w') as f:
        f.write("未捕获的异常:\n")
        f.write(f"类型: {exc_type.__name__}\n")
        f.write(f"值: {exc_value}\n")
        f.write(f"追踪信息: {exc_traceback}\n")

sys.excepthook = log_exception  # 设置未捕获异常的处理程序

# 函数调用部分

script_directory = get_program_path()  # 获取脚本所在目录
config_path = os.path.join(script_directory, 'config.json')  # 生成绝对路径
print(script_directory)
print(config_path)

print("Python Version:", sys.version)
if not os.path.exists(config_path):
    SID, password, isAutoStart = initP(True)
    config = {
        "SID": SID,
        "password": password,
        "isAutoStart": isAutoStart
    }
    if isAutoStart:
        autoStart()
    else:
        print("未选择开机自启，请手动添加开机自启")

    initC(config)
    print(f"config.json的绝对路径是: {config_path}")

wifi_name = "HNIU"

max_retries = 10
retry_count = 0
while retry_count < max_retries:
    try:
        if connect_to_wifi(wifi_name):
            logger.info("成功连接到 WiFi: HNIU")
            printLog()
            time.sleep(2)
            with open(config_path) as f:
                config = json.load(f)
                S = config["SID"]
                P = config["password"]
            loginSuccess = Login(S, P)
            print(loginSuccess)
            for i in range(10):
                if loginSuccess:
                    printLog(3)
                    logger.info("登录成功")
                    break
                logger.error(f"登录失败，尝试第{i+1}次")
                print(f"{Fore.RED}[Error]{Fore.WHITE}登录失败")
                print(f"{Fore.YELLOW}尝试第{i+1}次尝试连接到校园网...")
                loginSuccess = Login(S, P)
                time.sleep(2)
            else:
                printLog(2)
                logger.error(f"登录失败,您的学号是{S}\n您的密码是{P}")
                print(f"登录失败,您的学号是{Fore.GREEN+S+Fore.WHITE}\n您的密码是{Fore.GREEN+P}")
                isorno = selectTorF("是否重新输入学号？（方向键下选择↓,回车确认）", "否", "是")
                if isorno:
                    a, b, c = initP(False)
                    config = {
                        "SID": a,
                        "password": b,
                        "isAutoStart": c
                    }
                    initC(config)
                    loginSuccess = Login(a, b)
                    if loginSuccess:
                        printLog(3)
                        logger.info("登录成功")
        
            break  # 成功连接并登录后退出循环
        else:
            logger.error("连接失败，您可以寻找开发者解决或者是自行检查")
            print("连接失败，您可以寻找开发者解决或者是自行检查")
            break  # 连接失败后退出循环
    except requests.exceptions.ConnectionError as e:
        retry_count += 1
        logger.error(f"DNS解析失败或连接错误: {e}, 尝试重连 {retry_count}/{max_retries}")
        print(f"{Fore.RED}[Error]{Fore.WHITE} DNS解析失败或连接错误: {e}, 尝试重连 {retry_count}/{max_retries}")
        time.sleep(3)  # 等待2秒后重试1
else:
    logger.error("达到最大重试次数，放弃连接")
    print(f"{Fore.RED}[Error]{Fore.WHITE} 达到最大重试次数，放弃连接")


input("点击回车退出程序")

# os.system("taskkill /F /IM msedge.exe")#杀死校园网自启动的登录页面

# input1.send_keys((password))
# print("a",type(input0))

"""
/html/body/div[1]/div/div[2]/div[4]/form/input[2]

/html/body/div[1]/div/div[2]/div[4]/form/input[3]

/html/body/div[1]/div/div[2]/div[4]/select

//*[@id="edit_body"]/div[1]/div[1]/form/div
/html/body/div/div/div[1]/div[1]/form/div
/html/body/div/div/div[1]/div[1]/form/div
/html/body/div[1]/div/div[1]/div[1]/form/div
config
{
    SID:"",
    password:"xxxx",
    isAutoStart:0
}


25/3/16  v1.4这个版本应该没问题了，之前写的全是bug。。。到时候重构下（会的吧
"""

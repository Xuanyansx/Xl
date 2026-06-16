from pydoc import text
import subprocess
import os
import sys
import time
import keyboard
import winreg as reg
import simplejson as json
import requests
from colorama import init, Fore, Style

"""

AutoWifi v1.1版本

"""

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
    try :
        requests.post(url, data=data)
    except requests.RequestException as e:
        print(f"{e}，尝试重新连接")
        for i in range(5):
            requests.post(url, data=data)
    print()


with open('config.json') as f:
    config = json.load(f)
    S = config["SID"]
    P = config["password"]
    if connect_to_wifi('HNIU'):
        time.sleep(3)
        Login(S,P)


input()
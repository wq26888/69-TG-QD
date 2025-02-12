import os
import json
import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# 配置文件路径
config_file_path = "config.json"
签到结果 = ""

# 获取html中的用户信息
def fetch_and_extract_info(domain,headers):
    url = f"{domain}/user"

    # 发起 GET 请求
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("用户信息获取失败，页面打开异常.")
        return None

    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有 script 标签
    script_tags = soup.find_all('script')

    # 提取 ChatraIntegration 的 script 内容
    chatra_script = None
    for script in script_tags:
        if 'window.ChatraIntegration' in str(script):
            chatra_script = script.string
            break

    if not chatra_script:
        print("未识别到用户信息")
        return None

    # 使用正则表达式提取需要的信息
    # 提取用户名、邮箱、到期时间和剩余流量
    user_info = {}
    # user_info['用户名'] = re.search(r"name: '(.*?)'", chatra_script).group(1) if re.search(r"name: '(.*?)'", chatra_script) else None
    # user_info['邮箱'] = re.search(r"email: '(.*?)'", chatra_script).group(1) if re.search(r"email: '(.*?)'", chatra_script) else None
    user_info['到期时间'] = re.search(r"'Class_Expire': '(.*?)'", chatra_script).group(1) if re.search(r"'Class_Expire': '(.*?)'", chatra_script) else None
    user_info['剩余流量'] = re.search(r"'Unused_Traffic': '(.*?)'", chatra_script).group(1) if re.search(r"'Unused_Traffic': '(.*?)'", chatra_script) else None

    # 输出用户信息
    用户信息 = f"到期时间: {user_info['到期时间']}\n剩余流量: {user_info['剩余流量']}\n"
    # print(f"到期时间: {user_info['到期时间']}")
    # print(f"剩余流量: {user_info['剩余流量']}")

    # 提取 Clash 订阅链接
    clash_link = None
    for script in script_tags:
        if 'index.oneclickImport' in str(script) and 'clash' in str(script):
            link = re.search(r"'https://checkhere.top/link/(.*?)\?sub=1'", str(script))
            if link:
                用户信息 += f"Clash 订阅链接: https://checkhere.top/link/{link.group(1)}?clash=1\nv2ray 订阅链接: https://checkhere.top/link/{link.group(1)}?sub=3\n\n"
                # print(f"Clash 订阅链接: https://checkhere.top/link/{link.group(1)}?clash=1")
                # print(f"v2ray 订阅链接: https://checkhere.top/link/{link.group(1)}?sub=3")
                break
    return 用户信息

def generate_config():
    # 获取环境变量
    domain = os.getenv('DOMAIN', 'https://69yun69.com')  # 默认值，如果未设置环境变量
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    # if not bot_token or not chat_id:
        # raise ValueError("BOT_TOKEN 和 CHAT_ID 是必需的环境变量。")

    # 获取用户和密码的环境变量
    accounts = []
    index = 1

    while True:
        user = os.getenv(f'USER{index}')
        password = os.getenv(f'PASS{index}')

        if not user or not password:
            break  # 如果没有找到更多的用户信息，则退出循环

        accounts.append({
            'user': user,
            'pass': password
        })
        index += 1

    # 构造配置数据
    config = {
        'domain': domain,
        'BotToken': bot_token,
        'ChatID': chat_id,
        'accounts': accounts
    }
    print(config)
    return config


# 发送消息到 Telegram Bot 的函数，支持按钮
def send_message(msg="", BotToken="", ChatID=""):
    # 获取当前 UTC 时间，并转换为北京时间（+8小时）
    now = datetime.utcnow()
    beijing_time = now + timedelta(hours=8)
    formatted_time = beijing_time.strftime("%Y-%m-%d %H:%M:%S")

    # 打印调试信息
    # print(msg)

    # 如果 Telegram Bot Token 和 Chat ID 都配置了，则发送消息
    if BotToken != '' and ChatID != '':
        # 构建消息内容
        message_text = f"执行时间: {formatted_time}\n{msg}"

        # 构造按钮的键盘布局
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "一休交流群",
                        "url": "https://t.me/yxjsjl"
                    }
                ]
            ]
        }

        # 发送消息时附带内联按钮
        url = f"https://api.telegram.org/bot{BotToken}/sendMessage"
        payload = {
            "chat_id": ChatID,
            "text": message_text,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(keyboard)
        }

        try:
            # 发送 POST 请求
            response = requests.post(url, data=payload)
            return response
        except Exception as e:
            print(f"发送电报消息时发生错误: {str(e)}")
            return None

# 登录并签到的主要函数
def checkin(account, domain, BotToken, ChatID):
    user = account['user']
    pass_ = account['pass']

    签到结果 = f"地址: {domain[:9]}****{domain[-5:]}\n账号: {user[:1]}****{user[-5:]}\n密码: {pass_[:1]}****{pass_[-1]}\n\n"

    try:
        # 检查必要的配置参数是否存在
        if not domain or not user or not pass_:
            raise ValueError('必需的配置参数缺失')

        # 登录请求的 URL
        login_url = f"{domain}/auth/login"

        # 登录请求的 Payload（请求体）
        login_data = {
            'email': user,
            'passwd': pass_,
            'remember_me': 'on',
            'code': "",
        }

        # 设置请求头
        login_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Origin': domain,
            'Referer': f"{domain}/auth/login",
        }

        # 发送登录请求
        login_response = requests.post(login_url, json=login_data, headers=login_headers)

        print(f'{user}账号登录状态:', login_response.status_code)

        # 如果响应状态不是200，表示登录失败
        if login_response.status_code != 200:
            raise ValueError(f"登录请求失败: {login_response.text}")

        # 解析登录响应的 JSON 数据
        login_json = login_response.json()
        # print(f'{user}账号登录后返回的用户信息:', login_json)

        # 检查登录是否成功
        if login_json.get("ret") != 1:
            raise ValueError(f"登录失败: {login_json.get('msg', '未知错误')}")

        # 获取登录成功后的 Cookie
        cookies = login_response.cookies
        if not cookies:
            raise ValueError('登录成功但未收到Cookie')

        # print('Received cookies:', cookies)

        # 等待确保登录状态生效
        time.sleep(1)

        # 签到请求的 URL
        checkin_url = f"{domain}/user/checkin"

        # 签到请求的 Headers
        checkin_headers = {
            'Cookie': '; '.join([f"{key}={value}" for key, value in cookies.items()]),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': domain,
            'Referer': f"{domain}/user/panel",
            'X-Requested-With': 'XMLHttpRequest'
        }

        # 发送签到请求
        checkin_response = requests.post(checkin_url, headers=checkin_headers)

        print(f'{user}账号签到状态:', checkin_response.status_code)

        # 获取签到请求的响应内容
        response_text = checkin_response.text
        # print(f'{user}账号签到响应内容:', response_text)


        try:
            # 尝试解析签到的 JSON 响应
            checkin_result = checkin_response.json()
            # print(f'{user}账号签到后的json信息:', checkin_result)
            账号信息 = f"地址: {domain}\n账号: {user}\n密码: <tg-spoiler>{pass_}</tg-spoiler>\n"

            用户信息 = fetch_and_extract_info(domain,checkin_headers)

            # 账号信息的展示，注意密码用 <tg-spoiler> 标签隐藏
            # 根据返回的结果更新签到信息
            if checkin_result.get('ret') == 1 or checkin_result.get('ret') == 0:
                签到结果 = f"🎉 签到结果 🎉\n {checkin_result.get('msg', '签到成功' if checkin_result['ret'] == 1 else '签到失败')}"
            else:
                签到结果 = f"🎉 签到结果 🎉\n {checkin_result.get('msg', '签到结果未知')}"
        except Exception as e:
            # 如果出现解析错误，检查是否由于登录失效
            if "登录" in response_text:
                raise ValueError('登录状态无效，请检查Cookie处理')
            raise ValueError(f"解析签到响应失败: {str(e)}\n\n原始响应: {response_text}")

        # 发送签到结果到 Telegram
        send_message(账号信息 + 用户信息 + 签到结果, BotToken, ChatID)
        return 签到结果

    except Exception as error:
        # 捕获异常，打印错误并发送错误信息到 Telegram
        print(f'{user}账号签到异常:', error)
        签到结果 = f"签到过程发生错误: {error}"
        send_message(签到结果, BotToken, ChatID)
        return 签到结果

# 主程序执行逻辑
if __name__ == "__main__":

    # 读取配置
    config = generate_config()

    # 读取全局配置
    domain = config['domain']
    BotToken = config['BotToken']
    ChatID = config['ChatID']

    # 循环执行每个账号的签到任务
    for account in config.get("accounts", []):
        print("----------------------------------签到信息----------------------------------")
        print(checkin(account, domain, BotToken, ChatID))
        print("---------------------------------------------------------------------------")
# 在generate_config函数中添加邮件配置
def generate_config():

    # 添加邮件配置
    email_sender = os.getenv('EMAIL_SENDER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_receiver = os.getenv('EMAIL_RECEIVER')
    
    config = {
        'domain': domain,
        'BotToken': bot_token,
        'ChatID': chat_id,
        'accounts': accounts,
        'email': {
            'sender': email_sender,
            'password': email_password,
            'receiver': email_receiver
        }
    }
    return config

# 添加邮件发送函数
def send_email(subject, content, email_config):
    """
    发送邮件的函数
    :param subject: 邮件主题
    :param content: 邮件内容
    :param email_config: 邮件配置信息
    """
    if not all([email_config.get('sender'), email_config.get('password'), email_config.get('receiver')]):
        print("邮件配置信息不完整，跳过邮件发送")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = Header(email_config['sender'])
        msg['To'] = Header(email_config['receiver'])
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 连接Outlook SMTP服务器
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_config['sender'], email_config['password'])
        
        # 发送邮件
        server.sendmail(email_config['sender'], email_config['receiver'], msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"发送邮件时发生错误: {str(e)}")

# 在checkin函数中添加邮件发送
def checkin(account, domain, BotToken, ChatID, email_config=None):
    # ...现有代码...
    
    try:
        # ...现有代码...
        
        # 在发送Telegram消息后添加邮件发送
        if email_config:
            send_email(
                subject="69云签到结果",
                content=f"执行时间: {formatted_time}\n{账号信息}{用户信息}{签到结果}",
                email_config=email_config
            )
        
        return 签到结果
    
    except Exception as error:

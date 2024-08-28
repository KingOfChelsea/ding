import requests
import re
import json
import html
from bs4 import BeautifulSoup
def simulate_login(main_data):
    response = requests.get('https://www.mabangerp.com/index.htm')
    cookies = response.cookies
    # print(cookies)
    # 输出cookies
    # 获取cookies并将它们转换为类似你提供的字符串形式
    cookies = response.cookies
    cookie_string = '; '.join([f'{cookie.name}={cookie.value}' for cookie in cookies])
    url = 'https://www.mabangerp.com/index.php?mod=main.doLogin'
    Headers ={
    "Accept": "application/json, text/javascript, */*; q=0.01",
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie':cookie_string,
    "X-Requested-With": "XMLHttpRequest"
}
    
    #构造Session
    session = requests.Session()    
    # 发送 POST 请求
    response = session.post(url, headers=Headers, data=main_data)
    
    # 解析响应内容
    r = response.json()
    
    if r['success']:
        # 如果登录成功，模拟设置 cookie 的操作
        print("登录成功")
        return True
        # 你可以在这里处理成功后的逻辑，例如重定向用户
    elif 'errCode' in r and r['errCode'] == 'CHECK_VERIFY_CODE':
        # 如果需要验证码验证
        print("需要验证码验证")
        # 模拟显示验证码或处理验证码的逻辑
        try:
            print("显示验证码")
            # 调用你自己的验证码处理函数
        except Exception as e:
            print("验证码处理错误:", str(e))
    else:
        # 处理其他错误
        print("登录失败:", r.get('message'))
        return False
        if 'links' in r and r['links']:
            for item in r['links']:
                print(f"相关链接: {item['url']} - {item['text']}")
        

# 示例调用
main_data = {
    "username": "15577730705",  # 替换为实际用户名
    "password": "AFmd2580.",  # 替换为实际密码
    "allowImageCode": "1",
    "remember": "1"               # 是否记住登录状态，1 为记住，0 为不记住
}
log = simulate_login(main_data)
login_url = 'https://www.mabangerp.com/index.php?mod=main.doLogin'
payload = {
    "username": "15577730705",  # 替换为实际用户名
    "password": "Afmd2580.",  # 替换为实际密码
    "remeber": 1,               # 是否记住登录状态，1 为记住，0 为不记住
    "alowImageCode": 1          # 是否允许图片验证码，0 为不允许，1 为允许
}
Headers ={
    "Accept": "application/json, text/javascript, */*; q=0.01",
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    # 'Cookie':cookie_string,
    "X-Requested-With": "XMLHttpRequest"
}
if(log==True):
    response = requests.post(url,headers=Headers, data=payload)

    # https://aamz.mabangerp.com/index.php?mod=finance.purchacefs&cMKey=afcfa36e7d78f4c4736fa73207aac4b3&searchValue=&searchType=&lang=cn
    response = requests.get('https://aamz.mabangerp.com/index.php?mod=finance.purchacefs&cMKey=afcfa36e7d78f4c4736fa73207aac4b3&searchValue=&searchType=&lang=cn')
    cookies = response.cookies
    cookie_string = '; '.join([f'{cookie.name}={cookie.value}' for cookie in cookies])

    def send_dingding_message(webhook, content, at_mobiles,person):
        headers = {
            'Content-Type': 'application/json'
        }

        at_text = ' '.join([f'@{mobile}' for mobile in at_mobiles])

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": f"📢 新任务通知: {content}",
                "text": (
                    f"### 📋 Hi {person} 您有一个马帮付款单待审核\n"
                    f"**任务内容:**\n"
                    f">#### {content} \n\n"
                    f"**分配给:**\n"
                    f"{at_text}\n\n"
                    f"**请尽快处理!谢谢**\n"
                    f"---\n"
                    f"*来自系统自动通知*"
                ),
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": False
            }
        }

        response = requests.post(webhook, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print('消息发送成功')
        else:
            print(f'消息发送失败，状态码: {response.status_code}')


    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=7d827cc4ff23dbe82b5af664a434aec175b8ea872b26d414de9daa028b4f783f'
    url = "https://aamz.mabangerp.com/index.php?mod=finance.financenewsearch"
    headers ={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Cookie':cookie_string
    }

    response = requests.get(url, headers=headers)
    data1 = response.content.decode()
    data_dict = json.loads(data1)
    text = data_dict['html']
    soup = BeautifulSoup(text, 'html.parser')
    getcheckFinLogList = "https://aamz.mabangerp.com/index.php?mod=finance.getcheckFinLogList"
    Headers ={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Cookie':cookie_string,
        "X-Requested-With": "XMLHttpRequest"
    }

    items_ul = soup.select('.li_content ul ')
    # amount_money = soup.select('.Amount-money')
    # print(amount_money)
    # 发起 POST 请求
    # 统计每个处理人的订单数量
    order_counts = {
        "TankZhang": {"count": 0, "orders": [], "phone": "18734857039"},
        "VincenYang": {"count": 0, "orders": [], "phone": "15889953080"},
        "TieliangWang": {"count": 0, "orders": [], "phone": "13333575161"},
        "MichaelWong":{"count": 0, "orders": [], "phone": "18664719900"}
    }

    next_person = {
        "TankZhang": "VincenYang",
        "VincenYang": "TieliangWang",
        "TieliangWang": "MichaelWong",
        "AotyZhao": "TankZhang",
        "PallenCheng": "TankZhang",
        "jackson": "TankZhang"
    }

    for ul in items_ul:
        first_input = ul.select('li')[1]
        first_input = first_input.select_one('a span').text
        first_input = json.loads(first_input)

        if first_input["status"] == 1 and not first_input["orderNum"].startswith("FY"):
            id = first_input["id"]
            order_num = first_input["orderNum"]
            total_amount = first_input["totalAmount"]

            data = {
                "id": id
            }
            response = requests.post(getcheckFinLogList, headers=Headers, data=data)
            data = response.content.decode() 
            data = json.loads(data)
            
            if data["success"] == True:
                soup = BeautifulSoup(data["html"], 'html.parser')
                match = re.search(r'<td class="text-center" width="15%">(.*?)</td>', html.unescape(data.get("html", "")))
                
                if match:
                    result = match.group(1).strip()
                    print(result)

                    # 规则：如果配对到 TieliangWang 并且 totalAmount 大于 1000，增加 MichaelWong 的订单数量
                    if result == "TieliangWang" and total_amount > 1000:
                        order_counts["MichaelWong"]["count"] += 1
                        order_counts["MichaelWong"]["orders"].append(order_num)
                    elif result in next_person:
                        next_person_key = next_person[result]
                        order_counts[next_person_key]["count"] += 1
                        order_counts[next_person_key]["orders"].append(order_num)

    # 输出结果并发送消息
    for person, details in order_counts.items():
        if details["count"] > 0:
            orders = ', '.join(details["orders"])
            message = f"{person} 你有 {details['count']} 笔财务-付款单（待审核），订单编号：{orders}"
            print(message)
            # send_dingding_message(webhook_url, message, [details["phone"]], person)
        else:
            print(f"{person} 0 笔订单需要处理")

import requests
import re
import json
import html
from bs4 import BeautifulSoup

def send_dingding_message(webhook, content, at_mobiles, person):
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

def simulate_login(main_data):
    response = requests.get('https://www.mabangerp.com/index.htm')
    cookies = response.cookies

    cookie_string = '; '.join([f'{cookie.name}={cookie.value}' for cookie in cookies])

    url = 'https://www.mabangerp.com/index.php?mod=main.doLogin'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Cookie': cookie_string,
        "X-Requested-With": "XMLHttpRequest"
    }
    
    session = requests.Session()    
    response = session.post(url, headers=headers, data=main_data)
    r = response.json()
    
    if r.get('success'):
        print("登录成功")
        return session
    else:
        print("登录失败:", r.get('message'))
        return None

def main():
    main_data = {
        "username": "15577730705",
        "password": "AFmd2580.",
        "allowImageCode": "1",
        "remember": "1"
    }

    session = simulate_login(main_data)
    
    if session:
        webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=7d827cc4ff23dbe82b5af664a434aec175b8ea872b26d414de9daa028b4f783f'
        cookie_string = '; '.join([f'{cookie.name}={cookie.value}' for cookie in session.cookies])
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Cookie': cookie_string
        }

        url = "https://aamz.mabangerp.com/index.php?mod=finance.financenewsearch"
        response = session.get(url, headers=headers)
        data_dict = response.json()
        
        text = data_dict.get('html', '')
        soup = BeautifulSoup(text, 'html.parser')
        items_ul = soup.select('.li_content ul')
        
        getcheckFinLogList = "https://aamz.mabangerp.com/index.php?mod=finance.getcheckFinLogList"
        
        order_counts = {
            "TankZhang": {"count": 0, "orders": [], "phone": "18734857039"},
            "VincenYang": {"count": 0, "orders": [], "phone": "15889953080"},
            "TieliangWang": {"count": 0, "orders": [], "phone": "13333575161"},
            "MichaelWong": {"count": 0, "orders": [], "phone": "18664719900"}
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

                data = {"id": id}
                response = session.post(getcheckFinLogList, headers=headers, data=data)
                data = response.json()
                
                if data.get("success"):
                    match = re.search(r'<td class="text-center" width="15%">(.*?)</td>', html.unescape(data.get("html", "")))
                    
                    if match:
                        result = match.group(1).strip()

                        if result == "TieliangWang" and float(total_amount) > 1000:
                            order_counts["MichaelWong"]["count"] += 1
                            order_counts["MichaelWong"]["orders"].append(order_num)
                        elif result in next_person:
                            next_person_key = next_person[result]
                            order_counts[next_person_key]["count"] += 1
                            order_counts[next_person_key]["orders"].append(order_num)

        for person, details in order_counts.items():
            if details["count"] > 0:
                orders = ', '.join(details["orders"])
                message = f"{person} 你有 {details['count']} 笔财务-付款单（待审核），订单编号：{orders}"
                print(message)
                send_dingding_message(webhook_url, message, [details["phone"]], person)
            else:
                print(f"{person} 0 笔订单需要处理")

if __name__ == "__main__":
    main()
